from src.data_structures.core.transaction import Transaction


class RemoveLiquidityTransaction(Transaction):

    def __init__(self, transaction_hash: str):

        super().__init__(transaction_hash=transaction_hash)


def main():

    transaction_hash = "0xd808b3f43b6525ceb22fe29370cbfbdf23d251546f1aec5517c67e073123f6a1"
    parsed_transaction = RemoveLiquidityTransaction(transaction_hash)
    print(parsed_transaction.__json__)


if __name__ == "__main__":
    main()
