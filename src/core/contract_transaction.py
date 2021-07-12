from typing import Dict

from web3.types import TxReceipt

from src.core.contract_method import ContractMethod
from src.core.transaction import Transaction
from src.utils.contract_utils import init_contract, address_is_contract

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


def main():
    import json

    # interacting with Curve CryptoSwap contract 0x331af2e331bd619defaa5dac6c038f53fcf9f785.
    # There are 6 sub-contract calls:
    # 1. WETH9 Contract 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 deposits
    #    0 WETH to Curve CryptoSwap
    # 2. TetherToken contract 0xdAC17F958D2ee523a2206206994597C13D831ec7 orchestrates
    #    transfer from user address 0x7a16fF8270133F063aAb6C9977183D9e72835428 to
    #    Curve CryptoSwap contract.
    # 3. TetherToken transfer orchestrates transfer between Curve CryptoSwap to
    #    TriCrypto Liquidity Pool contract 0x80466c64868E1ab14a1Ddf27A676C3fcBE638Fe5
    # 4. Curve LP Token base implementation contract 0xcA3d75aC011BF5aD07a98d02f18225F9bD9A6BDF
    #    orchestrates minting of LP tokens from ZERO ADDRESS to Curve CryptoSwap contract
    # 5. TriCrypto LP Contract adds liquidity on behalf of the Curve CryptoSwap contract
    # 6. Curve LP token base implementation contract orchestrates minted LP token transfer from
    #    Curve CryptoSwap to user address.
    tx_hash_str = "0xc77884d3af1782869772f57ecfadd62cc16087e0576092928eaaec4ada9bbfb3"
    parsed_tx = Transaction(tx_hash_str)

    # check if the to_address is a contract. from_address can also be a contract, but
    # the contract that is run is the one with the to_address.
    if not address_is_contract(parsed_tx.to_address):
        pass

    contract_tx_parser = ContractTransaction(
        contract_address=parsed_tx.to_address,
        methods=[]  # TODO: Add contract methods here!
    )

    parsed_tx = contract_tx_parser.parse_transaction(tx_hash=tx_hash_str)
    print(json.dumps(parsed_tx, indent=4))


if __name__ == "__main__":
    main()
