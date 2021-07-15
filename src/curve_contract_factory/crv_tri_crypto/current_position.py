from datetime import datetime

from brownie import network
from brownie.network.contract import Contract
from brownie.network.transaction import ContractNotFound
from brownie.network.transaction import TransactionNotFound
from brownie.network.transaction import TransactionReceipt

from src.curve_contract_factory.crv_tri_crypto.constants import TRICRYPTO_CONVEX_GAUGE
from src.curve_contract_factory.crv_tri_crypto.constants import TRICRYPTO_CURVE_GAUGE
from src.curve_contract_factory.crv_tri_crypto.constants import TRICRYPTO_LP_TOKEN
from src.curve_contract_factory.crv_tri_crypto.constants import TRICRYPTO_POOL_CONTRACT
from src.utils.coingecko_utils import get_prices_of_coins
from src.utils.constants import STRFTIME_FORMAT
from src.utils.contract_utils import init_contract


class CurrentPositionCalculator:
    def __init__(self, network_name: str = "mainnet"):

        if not network.is_connected():
            network.connect(network_name)

        self.curve_gauge_contracts = Contract.from_explorer(TRICRYPTO_CURVE_GAUGE)
        self.convex_gauge_contracts = Contract.from_explorer(TRICRYPTO_CONVEX_GAUGE)
        self.pool_contract = Contract.from_explorer(TRICRYPTO_POOL_CONTRACT)
        self.pool_token_contract = Contract.from_explorer(TRICRYPTO_LP_TOKEN)

    def get_current_position(self, user_address: str, currency: str = "usd"):

        gauge_bal_convex = self.__get_convex_gauge_bal(user_address)
        gauge_bal_curve = self.__get_curve_gauge_bal(user_address)
        lp_token_bal = self.__get_lp_token_bal(user_address)
        gauge_bal = gauge_bal_convex + gauge_bal_curve
        token_balance_to_calc_on = gauge_bal + lp_token_bal

        time_now = datetime.utcnow()
        time_now_str = time_now.strftime(STRFTIME_FORMAT)

        # we calculate position on the following token balance
        # (tokens in gauge + free lp tokens)
        if not token_balance_to_calc_on:
            return {time_now: {}}

        token_prices_coingecko = get_prices_of_coins(currency=currency)

        # calculating position of coins in LP:
        # TODO: currently the following is hardcoded to tricrypto.
        #  make it more flexible.
        # this will ensure that the code is prepared for other curve v2
        token_names = ["USDT", "WBTC", "ETH"]
        final_positions = {}
        for i in range(len(token_names)):

            _token = init_contract(
                self.token_contract(i, tricrypto_contract=self.pool_contract)
            )
            _token_decimals = _token.functions.decimals().call()
            _price = 1
            price_from_curve_oracle = _price
            if token_names[i] not in ["USDT"]:
                price_from_curve_oracle = self.price_oracle(
                    token_index=i - 1, tricrypto_contract=self.pool_contract
                )
                _price = price_from_curve_oracle / 10 ** 18  # 18 digit precision

            _coins = (
                self.calc_withdraw_one_coin(
                    token_balance_to_calc_on, i, tricrypto_contract=self.pool_contract
                )
                / 10 ** _token_decimals
            )
            _val = _coins * _price
            position_data = {
                "token_contract_address": _token.address,
                "curve_oracle_price_usd": _price,
                "num_tokens": _coins,
                "value_tokens_usd": _val,
                "coingecko_price": {
                    currency: token_prices_coingecko[currency][token_names[i]]
                },
            }
            final_positions[token_names[i]] = position_data

        timestamped_output = {time_now: final_positions}

        return timestamped_output

    def get_curve_gauge_bal(self, address: str):
        contract = init_contract(self.curve_gauge_contracts)
        return contract.functions.balanceOf(address).call()

    def get_convex_gauge_bal(self, address: str):
        contract = init_contract(self.convex_gauge_contracts)
        return contract.functions.balanceOf(address).call()

    def get_lp_token_bal(self, address: str):
        contract = init_contract(self.pool_token_contract)
        return contract.functions.balanceOf(address).call()

    def calc_withdraw_one_coin(
        self, balance: int, token_index: int, tricrypto_contract
    ):
        return tricrypto_contract.functions.calc_withdraw_one_coin(
            balance, token_index
        ).call()

    def price_oracle(self, token_index: int, tricrypto_contract):
        return tricrypto_contract.functions.price_oracle(token_index).call()

    def token_contract(self, token_index: int, tricrypto_contract):
        return tricrypto_contract.functions.coins(token_index).call()
