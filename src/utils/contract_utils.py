import os

from etherscan.accounts import Account
from etherscan.client import Client
from etherscan.contracts import Contract as EtherscanContract
from hexbytes import HexBytes
from web3 import Web3

from src.utils.misc_utils import w3_infura


def init_contract(address: str):

    address = Web3.toChecksumAddress(address)
    contract_abi = EtherscanContract(
        address=address,
        api_key=os.environ["ETHERSCAN_API_KEY"],
    ).get_abi()
    contract = w3_infura.eth.contract(address=address, abi=contract_abi)
    return contract


class EtherscanContractExtended(Account):
    def __init__(self, address=Client.dao_address, api_key="YourApiKey"):
        Account.__init__(self, address=address, api_key=api_key)
        self.url_dict[self.MODULE] = "account"

    def get_tx_with(
        self,
        addr: str,
        start_block: int = 0,
        end_block: int = -1,
        sort: str = "asc",
    ):

        self.url_dict[self.ACTION] = "txlist"
        self.url_dict[self.SORT] = sort
        self.url_dict[self.START_BLOCK] = str(start_block)
        self.url_dict[self.END_BLOCK] = str(end_block)
        if int(end_block) == -1:
            self.url_dict[self.END_BLOCK] = "latest"

        self.build_url()
        req = self.connect()
        relevant_txes = []
        for tx in req["result"]:
            if tx["from"] in [
                addr,
                addr.lower(),
                Web3.toChecksumAddress(addr),
            ]:
                relevant_txes.append(tx)

        return relevant_txes


def address_is_contract(address: str) -> bool:
    return w3_infura.eth.getCode(address) > HexBytes(0)
