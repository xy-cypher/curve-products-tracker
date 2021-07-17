import logging
from typing import List

from brownie import network

from src.core.sanity_check.check_value import is_dust
from src.utils.contract_utils import init_contract


logging.getLogger(__name__)


class CurrentPositionCalculator:
    def __init__(
        self,
        pool_token_tickers: List,
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

        self.pool_token_tickers = pool_token_tickers

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
