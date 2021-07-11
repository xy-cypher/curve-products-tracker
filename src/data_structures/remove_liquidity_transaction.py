from src.data_structures.core.transaction import Transaction
from src.utils.constants import TRICRYPTO_LP_TOKEN_ADDR
from src.utils.exceptions import IncorrectContractException


class RemoveLiquidityTransaction(Transaction):

    def __init__(self, transaction_hash: str):

        super().__init__(transaction_hash=transaction_hash)
        self.removed_lp_tokens = 0
        self.get_removed_lp_tokens()

    def get_removed_lp_tokens(self):

        if self.logs_are_processed:
            return self.minted_lp_tokens

        log_to_process = self.tx_receipt["logs"][0]
        try:
            processed_log = TRICRYPTO_LP_TOKEN_ADDR.events.Transfer().processLog(log_to_process)
        except Exception as e:
            raise IncorrectContractException

        self.removed_lp_tokens = processed_log["args"]["_value"]
        self.logs_are_processed = True


def main():

    transaction_hash = "0xd808b3f43b6525ceb22fe29370cbfbdf23d251546f1aec5517c67e073123f6a1"
    parsed_transaction = RemoveLiquidityTransaction(transaction_hash)
    print(parsed_transaction.__json__)


if __name__ == "__main__":
    main()
