import web3 as web3

from src.core.contract_transaction import ContractTransaction, parse_logs
from src.core.method_event import SubContractEvent
from src.core.transaction import Transaction
from src.curve_contract_factory.crv_tri_crypto.constants import \
    TRICRYPTO_LP_TOKEN
from src.curve_contract_factory.crv_tri_crypto.constants import \
    TRICRYPTO_POOL_CONTRACT
from src.utils.contract_utils import init_contract


class CrvTriCrypto:
    def __init__(
            self,
            pool_contract: web3.eth.contract = TRICRYPTO_POOL_CONTRACT,
            token_contract: web3.eth.contract = TRICRYPTO_LP_TOKEN
    ):
        self.pool_contract = pool_contract
        self.token_contract = token_contract

        self.__set_sub_contract_events()

    def __set_sub_contract_events(self):
        # TODO: Add method of liquidity added in all coins

        self.event_dict = {
            "add_liquidity": SubContractEvent(
                contract_address=self.token_contract.address,
                contract_name="curve_base_lp_token",
                event_name="Transfer",
            ),
            "remove_liquidity": SubContractEvent(
                contract_address=self.pool_contract.address,
                contract_name="tricrypto_lp",
                event_name="RemoveLiquidity",
            ),
            "remove_liquidity_one": SubContractEvent(
                contract_address=self.pool_contract.address,
                contract_name="tricrypto_lp",
                event_name="RemoveLiquidityOne",
            )
        }

    def parse_liquidity_transaction(self, tx_hash: str) -> dict:

        parsed_tx = Transaction(tx_hash)
        contract_tx_parser = ContractTransaction(
            contract_address=parsed_tx.tx_data.to,
        )
        method_name = contract_tx_parser.get_tx_method(parsed_tx)
        parsed_logs = parse_logs(
            tx_receipt=parsed_tx.tx_receipt,
            sub_contract_event=self.event_dict[method_name]
        )
        return self.__groom_parsed_tx(parsed_tx, parsed_logs)

    def __groom_parsed_tx(
            self,
            parsed_tx: dict,
            parsed_logs: dict
    ) -> dict:
        raise NotImplementedError

    def parse_swap_transaction(self):
        raise NotImplementedError


def main():
    pass


if __name__ == "__main__":
    main()
