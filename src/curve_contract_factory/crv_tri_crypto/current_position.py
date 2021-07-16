import logging
from datetime import datetime
from typing import Tuple

from brownie import network
from brownie.network.contract import Contract

from src.core.datastructures.coingecko_price import CoinGeckoPrice
from src.core.datastructures.current_position import CurrentPosition
from src.core.datastructures.fees import PoolFees
from src.core.datastructures.rewards import OutstandingRewards
from src.core.datastructures.tokens import Token
from src.curve_contract_factory.crv_tri_crypto.constants import (
    TRICRYPTO_CONVEX_GAUGE,
)
from src.curve_contract_factory.crv_tri_crypto.constants import (
    TRICRYPTO_CURVE_GAUGE,
)
from src.curve_contract_factory.crv_tri_crypto.constants import (
    TRICRYPTO_LP_TOKEN,
)
from src.curve_contract_factory.crv_tri_crypto.constants import (
    TRICRYPTO_POOL_CONTRACT,
)
from src.utils.coingecko_utils import get_prices_of_coins
from src.utils.contract_utils import init_contract


logging.getLogger(__name__)


class CurrentPositionCalculator:
    def __init__(self, network_name: str = "mainnet"):

        if not network.is_connected():
            network.connect(network_name)

        self.curve_gauge_contracts = Contract.from_explorer(
            TRICRYPTO_CURVE_GAUGE
        )
        self.convex_gauge_contracts = Contract.from_explorer(
            TRICRYPTO_CONVEX_GAUGE
        )
        self.pool_contract = Contract.from_explorer(TRICRYPTO_POOL_CONTRACT)
        self.pool_token_contract = Contract.from_explorer(TRICRYPTO_LP_TOKEN)

        self.pool_token_tickers = ["USDT", "WBTC", "ETH"]

    def get_current_position(self, user_address: str, currency: str = "usd"):

        time_now = datetime.utcnow()
        lp_token_balance, gauge_balance = self.get_token_and_gauge_bal(
            user_address=user_address
        )
        token_balance_to_calc_on = lp_token_balance + gauge_balance

        if not token_balance_to_calc_on:
            return None

        token_prices_coingecko = get_prices_of_coins(currency=currency)
        current_position_of_tokens = []
        for i in range(len(self.pool_token_tickers)):

            token_contract = init_contract(
                self.pool_contract.functions.coins(i).call()
            )
            token_decimals = token_contract.functions.decimals().call()
            oracle_price = 1
            if self.pool_token_tickers[i] != "USDT":
                price_oracle = self.pool_contract.functions.price_oracle(i)
                price_from_curve_oracle = price_oracle.call()(
                    token_index=i - 1, tricrypto_contract=self.pool_contract
                )
                oracle_price = price_from_curve_oracle * 1e-18

            num_tokens = (
                self.pool_contract.functions.calc_withdraw_one_coin(
                    token_balance_to_calc_on, i
                ).call()
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
                        quote=token_prices_coingecko[
                            self.pool_token_tickers[i]
                        ],
                    ),
                )
            )

        accrued_fees = self.calculate_accrued_fees(user_address=user_address)
        outstanding_rewards = self.calculate_outstanding_rewards(user_address)

        position_data = CurrentPosition(
            time=time_now,
            lp_tokens=lp_token_balance,
            gauge_tokens=gauge_balance,
            accrued_fees=accrued_fees,
            tokens=current_position_of_tokens,
            outstanding_rewards=outstanding_rewards,
        )

        return position_data

    def get_token_and_gauge_bal(
        self, user_address: str
    ) -> Tuple[float, float]:
        """We calculate position on the following token balance:
        (tokens in gauge + free lp tokens)

        :param user_address: web3 address of the user
        :return:
        """

        gauge_balance_convex = self.convex_gauge_contracts.functions.balanceOf(
            user_address
        ).call()
        gauge_balance_curve = self.curve_gauge_contracts.functions.balanceOf(
            user_address
        ).call()
        pool_token_balance = self.pool_token_contract.functions.balanceOf(
            user_address
        ).call()
        total_gauge_balance = gauge_balance_convex + gauge_balance_curve
        return total_gauge_balance, pool_token_balance

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
