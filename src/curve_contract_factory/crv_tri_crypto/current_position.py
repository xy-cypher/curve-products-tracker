import web3 as web3

from src.curve_contract_factory.crv_tri_crypto.constants import \
    TRICRYPTO_LP_TOKEN
from src.curve_contract_factory.crv_tri_crypto.constants import \
    TRICRYPTO_POOL_CONTRACT

from brownie.network.transaction import TransactionReceipt


class CrvTriCrypto:
    def __init__(
            self,
            pool_contract: web3.eth.contract = TRICRYPTO_POOL_CONTRACT,
            token_contract: web3.eth.contract = TRICRYPTO_LP_TOKEN
    ):
        self.pool_contract = pool_contract
        self.token_contract = token_contract

    def parse_liquidity_transaction(self, tx_hash: str) -> dict:

        TransactionReceipt()

        return


def main():
    pass


if __name__ == "__main__":
    main()
