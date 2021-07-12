from typing import Dict

from web3.types import TxReceipt

from src.core.contract_method import ContractMethod
from src.core.transaction import Transaction
from src.utils.contract_utils import init_contract

from web3 import Web3


class ContractTransaction:

    def __init__(self, contract_address: str, methods: Dict[ContractMethod]):

        if not Web3.isChecksumAddress(contract_address):
            contract_address = Web3.toChecksumAddress(contract_address)

        self.contract = init_contract(address=contract_address)
        self.contract_methods = methods

    def parse_transaction(self, tx_hash: str):

        parsed_transaction = Transaction(tx_hash)
        decoded_tx_input = self.contract.decode_function_input(
            parsed_transaction.tx_data.input
        )
        method_name = decoded_tx_input[0].__dict__["abi"]["name"]
        contract_method: ContractMethod = self.methods[method_name]
        tx_receipt: TxReceipt = parsed_transaction.tx_receipt
        decoded_event_logs = contract_method.decode_tx_receipt_logs(tx_receipt)

        return {
            "tx_overview": parsed_transaction.__dict__,
            "method_name": method_name,
            "logs": decoded_event_logs
        }


