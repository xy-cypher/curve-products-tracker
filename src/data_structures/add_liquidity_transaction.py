from src.data_structures.core.transaction import Transaction
from web3.exceptions import ABIEventFunctionNotFound, MismatchedABI

from src.utils.constants import TRICRYPTO_LP_TOKEN_ADDR
from src.utils.exceptions import IncorrectContractException


class AddLiquidityTransaction(Transaction):

    def __init__(self, transaction_hash: str):

        super().__init__(transaction_hash=transaction_hash)
        self.minted_lp_tokens = 0
        self.get_minted_lp_tokens()

    def get_minted_lp_tokens(self):

        if self.logs_are_processed:
            return self.minted_lp_tokens

        try:
            self.__minted_lp_tokens_deposit_contract()
        except IncorrectContractException:
            self.__minted_lp_tokens_pool_contract()
        self.logs_are_processed = True

    def __minted_lp_tokens_deposit_contract(self):

        log_to_process = self.tx_receipt["logs"][2]
        try:
            processed_log = TRICRYPTO_LP_TOKEN_ADDR.events.Transfer().processLog(log_to_process)
        except Exception as e:
            raise IncorrectContractException

        self.minted_lp_tokens = processed_log["args"]["_value"]

    def __minted_lp_tokens_pool_contract(self):

        log_to_process = self.tx_receipt["logs"][1]
        try:
            processed_log = (
                TRICRYPTO_LP_TOKEN_ADDR.events.Transfer().processLog(log_to_process)
            )
        except (ABIEventFunctionNotFound, MismatchedABI):
            raise IncorrectContractException
        self.minted_lp_tokens = processed_log["args"]["_value"]


def main():

    # tx with 0x331af2e331bd619defaa5dac6c038f53fcf9f785
    transaction_hash = "0xd557732dc9c2065140ddfe75c7b7dae8a4b9aaa95e628f199ed4938a1350b769"
    parsed_transaction = AddLiquidityTransaction(transaction_hash)
    print(parsed_transaction.__json__)

    # tx with 0x80466c64868e1ab14a1ddf27a676c3fcbe638fe5
    transaction_hash = "0xcc1695bab2ff8343e5b407aae3a97ea4ec37d9b5f4cb88847752eefaebfd0181"
    parsed_transaction = AddLiquidityTransaction(transaction_hash)
    print(parsed_transaction.__json__)


if __name__ == "__main__":
    main()
