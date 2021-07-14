from web3 import Web3
from web3.exceptions import MismatchedABI
from web3.types import TxReceipt

from src.core.method_event import SubContractEvent
from src.core.transaction import Transaction
from src.utils.contract_utils import init_contract


class ContractTransaction:
    def __init__(self, contract_address: str):

        if not Web3.isChecksumAddress(contract_address):
            contract_address = Web3.toChecksumAddress(contract_address)
        self.contract = init_contract(address=contract_address)

    def get_tx_method(self, parsed_transaction: TxReceipt):
        decoded_tx_input = self.contract.decode_function_input(
            parsed_transaction.tx_data.input,
        )
        method_name = decoded_tx_input[0].__dict__["abi"]["name"]
        return method_name

    def parse_transaction(
        self,
        tx_hash: str,
        sub_contract_event: SubContractEvent,
    ):

        parsed_transaction = Transaction(tx_hash)
        method_name = self.get_tx_method(parsed_transaction)
        parsed_logs = parse_logs(
            parsed_transaction.tx_receipt,
            sub_contract_event
        )

        parsed_tx = {
            "tx_overview": parsed_transaction.__parsed_dict__,
            "method_name": method_name,
            "logs": parsed_logs,
        }
        return parsed_tx


def parse_logs(
        tx_receipt: TxReceipt,
        sub_contract_event: SubContractEvent
):
    tx_receipt: TxReceipt = tx_receipt
    for log in tx_receipt.logs:
        try:
            processed_log = sub_contract_event.process_log(log)
            break
        except MismatchedABI:
            continue
    return processed_log
