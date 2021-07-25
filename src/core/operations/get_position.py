import logging
from datetime import datetime
from typing import Optional

import pytz
from brownie import web3

from src.core.datastructures.current_position import Position
from src.core.datastructures.tokens import Token
from src.core.products_factory import Product
from src.core.sanity_check.check_value import is_dust
from src.utils.constants import SUSHISWAP_ROUTER_CONTRACT as DEX_ROUTER_ADDR
from src.utils.constants import USDT
from src.utils.contract_utils import init_contract
from src.utils.redis_cacher import cache

logging.getLogger(__name__)


class CurvePositionCalculator:
    def __init__(
        self,
        product: Product,
    ):

        logging.info("Initialising Position Calculator ...")

        # todo: initialise using poolinfo or pool config yaml file

        self.pool_contract = init_contract(product.contract.addr)

        # initialise pool token contracts
        if len(product.token_contracts.items()) != 1:
            raise  # there should only be 1 token contract
        self.pool_token_contract = {}
        for token_name, info in product.token_contracts.items():

            token_contract = init_contract(info.addr)
            self.pool_token_contract = {
                "contract": token_contract,
                "decimals": token_contract.decimals(),
            }

        # get num underlying tokens
        self.num_underlying_tokens = 0
        for i in range(100):
            try:
                self.pool_contract.coins(i)
                self.num_underlying_tokens += 1
            except ValueError:  # max index reached, hence count is num tokens
                break

        # initialise auxiliary contracts:
        # NOTE: gauge tokens have the same decimals as lp tokens
        self.gauge_contracts = {}
        for contract_name, contract in product.other_contracts.items():

            contract_name: str = contract_name
            gauge_contract = None
            decimals = None
            if contract.addr:
                gauge_contract = init_contract(contract.addr)
                decimals = self.pool_token_contract["decimals"]

            gauge = {"contract": gauge_contract, "decimals": decimals}

            self.gauge_contracts[contract_name] = gauge

        # init sushiswap router contract for fetching prices wrt usdt
        self.dex_router = init_contract(DEX_ROUTER_ADDR)

        logging.info("... done!")

    def calc_max_withdrawable_lp_tokens(
        self, total_tokens: int, block_number: int
    ):
        """This is just to ensure that the total tokens a token holder has
        is actually withdrawable: if they are a whale, they may not be able
        to withdraw all of their liquidity but a certain percentage of it

        :param block_number:
        :param total_tokens:
        :return:
        """

        withdraw_fraction = [x * 0.01 for x in range(0, 101)[::-1]]
        for fraction in withdraw_fraction:
            try:
                num_withdrawable_lp_tokens = fraction * total_tokens
                _ = self.pool_contract.calc_withdraw_one_coin(
                    fraction * total_tokens, 0, block_identifier=block_number
                )
                return num_withdrawable_lp_tokens
            except ValueError:
                continue

        return 0

    def get_token_and_gauge_bal(
        self, user_address: str, block_number: int
    ) -> dict:
        """We calculate position on the following token balance:
        (tokens in gauge + free lp tokens)

        :param block_number:
        :param user_address: web3 address of the user
        :return:
        """
        token_balances = {}

        # liquidity pool token balances

        try:
            pool_token_balance = self.pool_token_contract[
                "contract"
            ].balanceOf(user_address, block_identifier=block_number)
            if is_dust(
                pool_token_balance, self.pool_token_contract["decimals"]
            ):
                pool_token_balance = 0
        except ValueError:
            pool_token_balance = 0

        token_balances["liquidity_pool"] = pool_token_balance

        # gauge token balances
        for name, gauge in self.gauge_contracts.items():
            if not gauge["contract"]:
                continue
            try:
                token_balance = gauge["contract"].balanceOf(
                    user_address, block_identifier=block_number
                )
                if is_dust(token_balance, gauge["decimals"]):
                    token_balance = 0
            except ValueError:
                token_balance = 0
            token_balances[name] = token_balance

        return token_balances

    def get_position(
        self,
        user_address: str,
        block_number: Optional[int],
    ) -> Position:  # todo: refactor position object to only accept time, numtokens price and thats it
        print()

        # todo:the following contract call can be removed
        tx_time = pytz.utc.localize(
            datetime.utcfromtimestamp(
                web3.eth.getBlock(block_number).timestamp
            )
        )
        platform_token_balances = self.get_token_and_gauge_bal(
            user_address=user_address, block_number=block_number
        )
        token_balance_to_calc_on = sum(platform_token_balances.values())

        # todo: consider alternatives to the following
        token_balance_to_calc_on = self.calc_max_withdrawable_lp_tokens(
            token_balance_to_calc_on, block_number=block_number
        )

        if not token_balance_to_calc_on:
            return Position(time=tx_time, block_number=block_number)

        current_position_of_tokens = []
        for i in range(self.num_underlying_tokens):

            # todo: redundant init contracts: can slow down code'''
            token_contract = init_contract(self.pool_contract.coins(i))

            # todo: token name and token decimals can be hardcoded'''
            token_name = token_contract.name()
            token_decimals = token_contract.decimals()

            # calculate how many tokens the user would get if they withdrew
            # all of their liquidity in a single coin.
            num_tokens = self.pool_contract.calc_withdraw_one_coin(
                token_balance_to_calc_on, i, block_identifier=block_number
            )

            num_tokens_float = num_tokens / 10 ** token_decimals

            # todo: remove this method entirely for now. mvp style.
            value_tokens = self.get_dex_price_wrt_usdt(
                num_tokens=num_tokens,
                token_in_addr=token_contract.address,
                block_number=block_number,
            )

            current_position_of_tokens.append(
                Token(
                    name=token_name,
                    address=token_contract.address,
                    num_tokens=num_tokens_float,
                    value_tokens=value_tokens,
                ),
            )

        platform_token_balances.update(
            (x, y / 10 ** self.pool_token_contract["decimals"])
            for x, y in platform_token_balances.items()
        )
        position_data = Position(
            time=tx_time,
            block_number=block_number,  # todo: maybe not needed
            token_balances=platform_token_balances,
            tokens=current_position_of_tokens,
        )

        return position_data

    # todo: can be its own function. prices can be queried w.r.t each other
    @cache
    def get_dex_price_wrt_usdt(
        self, num_tokens: int, token_in_addr: str, block_number: int
    ):

        # TODO: use curve pool get_dy method instead of sushiswap

        if token_in_addr == USDT.address:
            return num_tokens

        amounts_outs = self.dex_router.getAmountsOut(
            num_tokens,
            [token_in_addr, USDT.address],
            block_identifier=block_number,
        )

        return amounts_outs[1] / 10 ** USDT.decimals
