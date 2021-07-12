from typing import Dict

from web3.types import TxReceipt

from src.core.method_event import EventMethod


class ContractMethod:

    def __init__(self, method_name: str, event_methods: Dict[int: EventMethod]):

        self.method_name = method_name
        self.sub_contracts = event_methods

    def decode_tx_receipt_logs(self, tx_receipt: TxReceipt):

        decoded_event_logs = []
        for index, log in enumerate(tx_receipt["logs"]):

            event_method = self.event_methods[index]
            decoded_event_log = event_method.decode_log(log)
            decoded_event_logs.append(decoded_event_log)

        return decoded_event_logs
