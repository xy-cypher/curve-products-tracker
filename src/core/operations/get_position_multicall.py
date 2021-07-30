import logging
from typing import Any
from typing import Dict
from typing import List

import brownie

from src.core.datastructures.current_position import Position
from src.core.datastructures.tokens import Token
from src.core.products_factory import Product
from src.utils.contract_utils import init_contract

logging.getLogger(__name__)


class CurvePositionCalculatorMultiCall:
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

        # initialise underlying assets info
        self.lp_assets = []
        for i in range(100):
            try:
                asset_addr = self.pool_contract.coins(i)
                asset_contract = init_contract(asset_addr)
                asset_decimals = asset_contract.decimals()
                asset_name = asset_contract.name()
                self.lp_assets.append(
                    {
                        "name": asset_name,
                        "contract": asset_contract,
                        "decimals": asset_decimals,
                    }
                )
            except ValueError:  # max index reached
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

        logging.info("... done!")

    def get_position(self, lp_balances: dict, block_identifier: int) -> list:

        current_position_of_tokens = {}
        for asset_idx, asset in enumerate(self.lp_assets):

            # calculate how many tokens the user would get if they withdrew
            # all of their liquidity in a single coin.
            with brownie.multicall(
                address=self.pool_contract.address,
                block_identifier=block_identifier,
            ):
                num_tokens = [
                    self.pool_contract.calc_withdraw_one_coin(
                        lp_balance,
                        asset_idx,
                    )
                    for addr, lp_balance in lp_balances.items()
                ]

            num_tokens_float = [
                num_tokens_user / 10 ** asset["decimals"]
                for num_tokens_user in num_tokens
            ]
            current_position_of_tokens[asset["name"]] = num_tokens_float

        user_positions = self.__groom_user_positions(
            user_addrs=lp_balances.keys(),
            current_positions=current_position_of_tokens,
        )

        return user_positions

    @staticmethod
    def __groom_user_positions(
        user_addrs: Any, current_positions: Dict
    ) -> Dict:

        user_positions = {}
        for idx, addr in enumerate(user_addrs):
            user_position = {}
            for asset, positions in current_positions.items():
                user_position[asset] = positions[idx]

            user_positions[addr] = user_position

        return user_positions
