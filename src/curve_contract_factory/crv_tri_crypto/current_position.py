import logging
from datetime import datetime
from typing import Tuple

import pytz
from brownie import network
from brownie.exceptions import VirtualMachineError

from src.core.datastructures.coingecko_price import CoinGeckoPrice
from src.core.datastructures.current_position import CurrentPosition
from src.core.datastructures.fees import PoolFees
from src.core.datastructures.rewards import OutstandingRewards
from src.core.datastructures.tokens import Token
from src.core.sanity_check.check_value import is_dust
from src.utils.coingecko_utils import get_prices_of_coins
from src.utils.contract_utils import init_contract


logging.getLogger(__name__)


class CurrentPositionCalculator:
    def __init__(
        self,
        pool_contract: str,
        pool_token_contract: str,
        curve_gauge_contract: str,
        convex_gauge_contract: str,
        network_name: str = "mainnet",
    ):

        if not network.is_connected():
            network.connect(network_name)

        self.curve_gauge_contract = init_contract(curve_gauge_contract)

        # TODO: Remove this later as it is temporary code.
        self.convex_gauge_contract = None
        if self.convex_gauge_contract:
            self.convex_gauge_contract = init_contract(convex_gauge_contract)

        self.pool_contract = init_contract(pool_contract)
        self.pool_token_contract = init_contract(pool_token_contract)
        self.pool_token_decimals = self.pool_token_contract.decimals()

        self.pool_token_tickers = ["USDT", "WBTC", "ETH"]

    def get_current_position(self, user_address: str, currency: str = "usd"):

        time_now = pytz.utc.localize(datetime.utcnow())
        platform_token_balances = self.get_token_and_gauge_bal(
            user_address=user_address
        )
        token_balance_to_calc_on = sum(platform_token_balances.values())
        token_balance_to_calc_on = self.__calc_max_withdrawable_lp_tokens(
            token_balance_to_calc_on
        )

        if not token_balance_to_calc_on:
            return CurrentPosition(time=time_now)

        token_prices_coingecko = get_prices_of_coins(currency=currency)
        current_position_of_tokens = []
        for i in range(len(self.pool_token_tickers)):

            token_contract = init_contract(self.pool_contract.coins(i))
            token_decimals = token_contract.decimals()
            oracle_price = 1
            if self.pool_token_tickers[i] != "USDT":
                # there is no price oracle for USDT in the contract
                # and the first index is WBTC. Hence i-1 as i is 0 for USDT.
                price_from_curve_oracle = self.pool_contract.price_oracle(
                    i - 1
                )
                oracle_price = price_from_curve_oracle * 1e-18

            num_tokens = (
                self.pool_contract.calc_withdraw_one_coin(
                    token_balance_to_calc_on, i
                )
                / 10 ** token_decimals
            )

            value_tokens = num_tokens * oracle_price

            current_position_of_tokens.append(
                Token(
                    token=self.pool_token_tickers[i],
                    num_tokens=num_tokens,
                    value_tokens=value_tokens,
                    coingecko_price=CoinGeckoPrice(
                        currency=currency,
                        quote=token_prices_coingecko[currency][
                            self.pool_token_tickers[i]
                        ],
                    ),
                )
            )

        accrued_fees = self.calculate_accrued_fees(user_address=user_address)
        outstanding_rewards = self.calculate_outstanding_rewards(user_address)

        position_data = CurrentPosition(
            time=time_now,
            lp_tokens=platform_token_balances["liquidity_pool"]
            / 10 ** self.pool_token_decimals,
            curve_gauge_tokens=platform_token_balances["curve_gauge"]
            / 10 ** self.pool_token_decimals,
            convex_gauge_tokens=platform_token_balances["convex_gauge"]
            / 10 ** self.pool_token_decimals,
            accrued_fees=accrued_fees,
            tokens=current_position_of_tokens,
            outstanding_rewards=outstanding_rewards,
        )

        return position_data

    def __calc_max_withdrawable_lp_tokens(self, total_tokens):
        """This is just to ensure that the total tokens a token holder has
        is actually withdrawable: if they are a whale, they may not be able
        to withdraw all of their liquidity but a certain percentage of it

        :param total_tokens:
        :return:
        """

        withdraw_fraction = [x * 0.01 for x in range(0, 100)[::-1]]
        for fraction in withdraw_fraction:
            try:
                num_withdrawable_lp_tokens = fraction * total_tokens
                _ = self.pool_contract.calc_withdraw_one_coin(
                    fraction * total_tokens, 0
                )
                return num_withdrawable_lp_tokens
            except ValueError:
                continue

        return 0

    def get_token_and_gauge_bal(self, user_address: str) -> dict:
        """We calculate position on the following token balance:
        (tokens in gauge + free lp tokens)

        :param user_address: web3 address of the user
        :return:
        """
        gauge_balance_convex = 0
        if self.convex_gauge_contract:
            gauge_balance_convex = self.convex_gauge_contract.balanceOf(
                user_address
            )
            if is_dust(
                gauge_balance_convex, self.pool_token_contract.decimals()
            ):
                gauge_balance_convex = 0

        gauge_balance_curve = self.curve_gauge_contract.balanceOf(user_address)
        if is_dust(gauge_balance_curve, self.pool_token_contract.decimals()):
            gauge_balance_curve = 0

        pool_token_balance = self.pool_token_contract.balanceOf(user_address)
        if is_dust(pool_token_balance, self.pool_token_contract.decimals()):
            pool_token_balance = 0

        return {
            "convex_gauge": gauge_balance_convex,
            "curve_gauge": gauge_balance_curve,
            "liquidity_pool": pool_token_balance,
        }

    def calculate_accrued_fees(self, user_address: str) -> PoolFees:
        # TODO: calc accrued (unclaimed) fees
        logging.warning(
            f"Calculating PoolFees not implemented for {self.pool_contract}. "
            f"Returning empty PoolFees for {user_address}"
        )
        return PoolFees()

    def calculate_outstanding_rewards(
        self, user_address: str
    ) -> OutstandingRewards:
        # TODO: calc outstanding rewards
        logging.warning(
            f"Calculating OutstandingRewards not implemented for "
            f"{self.pool_contract}. Returning empty PoolFees for "
            f"{user_address}"
        )
        return PoolFees()
