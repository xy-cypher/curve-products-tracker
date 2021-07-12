from web3 import Web3

from src.utils.contract_utils import init_contract


class EventMethod:

    def __init__(self, contract_address: str, event_name: str, event_index: int):

        if not Web3.isChecksumAddress(contract_address):
            contract_address = Web3.toChecksumAddress(contract_address)

        self.contract = init_contract(address=contract_address)
        self.event_name = event_name
        self.event_index = event_index

    def decode_logs(self, log: dict):

        # TODO: Add generic decoding log logic here ...

        pass
