import logging
from datetime import datetime

import pytz

from src.core.datastructures.coingecko_price import CoinGeckoPrice
from src.core.datastructures.current_position import CurrentPosition
from src.core.datastructures.tokens import Token
from src.core.operations.get_current_position import CurrentPositionCalculator
from src.curve_contract_factory.crv_tri_crypto.constants import TRICRYPTO_v2_CONVEX_GAUGE
from src.curve_contract_factory.crv_tri_crypto.constants import TRICRYPTO_v2_CURVE_GAUGE
from src.curve_contract_factory.crv_tri_crypto.constants import TRICRYPTO_v2_LP_TOKEN
from src.curve_contract_factory.crv_tri_crypto.constants import TRICRYPTO_v2_POOL_CONTRACT
from src.utils.coingecko_utils import get_prices_of_coins
from src.utils.contract_utils import init_contract


logging.getLogger(__name__)


class TriCryptoCurrentPositionCalculator(CurrentPositionCalculator):
    def __init__(self, network_name: str = "mainnet"):

        super().__init__(
            pool_token_contract=TRICRYPTO_v2_LP_TOKEN,
            pool_contract=TRICRYPTO_v2_POOL_CONTRACT,
            curve_gauge_contract=TRICRYPTO_v2_CURVE_GAUGE,
            convex_gauge_contract=TRICRYPTO_v2_CONVEX_GAUGE,
            network_name=network_name,
            pool_token_tickers=["USDT", "WBTC", "ETH"],
        )

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
