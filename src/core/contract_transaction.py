from typing import List

from src.core.transaction import Transaction
from src.utils.contract_utils import address_is_contract, init_contract
from src.utils.exceptions import IncorrectContractException

import web3 as web3


class ContractTransaction(Transaction):

    def __init__(self, transaction_hash: str, log_decoders: List):

        super().__init__(transaction_hash=transaction_hash)

        self.log_decoders = log_decoders

        self.minted_lp_tokens = 0
        self.get_minted_lp_tokens()

        if not address_is_contract(self.to_address):
            raise

        self.contract_interacted_with = init_contract(address=self.to_address)
        self.decoded_tx_input = self.contract_interacted_with.decode_function_input(
            self.tx_data.input
        )
        self.method_name = self.decoded_tx_input[0].__dict__["abi"]["name"]