from typing import Dict

from web3.types import TxReceipt

from src.core.method_event import SubContractEvent


class ContractMethod:

    def __init__(self, method_name: str, event_methods: Dict[int: SubContractEvent]):

        self.method_name = method_name
        self.sub_contracts = event_methods

    def decode_tx_receipt_logs(self, tx_receipt: TxReceipt):

        decoded_event_logs = []
        for index, log in enumerate(tx_receipt["logs"]):

            event_method = self.event_methods[index]
            decoded_event_log = event_method.process_log(log)
            decoded_event_logs.append(decoded_event_log)

        return decoded_event_logs


def main():
    import json
    from src.core.transaction import Transaction

    # This is an example of add_liquidity method of the Curve CryptoSwap Deposit
    # Zap contract 0x331aF2E331bd619DefAa5DAc6c038f53FCF9F785
    tx_hash_str = "0xd557732dc9c2065140ddfe75c7b7dae8a4b9aaa95e628f199ed4938a1350b769"
    parsed_tx = Transaction(tx_hash_str)

    curve_cryptoswap_add_liquidity = ContractMethod(
        method_name="add_liquidity",
        event_methods=[]  # TODO: Add add_liquidity event methods here
    )

    logs = curve_cryptoswap_add_liquidity.decode_tx_receipt_logs(
        tx_receipt=parsed_tx.tx_receipt
    )
    print(json.dumps(logs, indent=4))


if __name__ == "__main__":
    main()
