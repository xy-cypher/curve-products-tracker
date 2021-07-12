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

    def parse_transaction(
        self,
        tx_hash: str,
        sub_contract_event: SubContractEvent,
    ):

        parsed_transaction = Transaction(tx_hash)
        tx_receipt: TxReceipt = parsed_transaction.tx_receipt
        decoded_tx_input = self.contract.decode_function_input(
            parsed_transaction.tx_data.input,
        )
        method_name = decoded_tx_input[0].__dict__["abi"]["name"]

        for log in tx_receipt.logs:

            try:
                processed_log = sub_contract_event.process_log(log)
                break
            except MismatchedABI:
                continue

        parsed_tx = {
            "tx_overview": parsed_transaction.__parsed_dict__,
            "method_name": method_name,
            "logs": processed_log,
        }
        return parsed_tx
