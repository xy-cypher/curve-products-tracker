from src.core.method_event import SubContractEvent
from src.curve_contract_factory.crv_tri_crypto.constants import TRICRYPTO_LP_TOKEN
from src.curve_contract_factory.crv_tri_crypto.constants import TRICRYPTO_POOL_CONTRACT
from src.utils.contract_utils import init_contract


class CrvTriCrypto:
    def __init__(self):

        self.pool_contract = TRICRYPTO_POOL_CONTRACT
        self.token_contract = TRICRYPTO_LP_TOKEN

        # TODO: Add method of liquidity added in all coins

        self.add_liquidity_event = SubContractEvent(
            contract_address=self.token_contract.address,
            contract_name="curve_base_lp_token",
            event_name="Transfer",
        )

        self.remove_liquidity_event = SubContractEvent(
            contract_address=self.pool_contract.address,
            contract_name="tricrypto_lp",
            event_name="RemoveLiquidity",
        )

        self.remove_liquidity_one_event = SubContractEvent(
            contract_address=self.pool_contract.address,
            contract_name="tricrypto_lp",
            event_name="RemoveLiquidityOne",
        )

    def parse_liquidity_transaction(self):

        raise NotImplementedError

    def parse_swap_transaction(self):

        raise NotImplementedError
