import os
from hexbytes import HexBytes

from etherscan.contracts import Contract as EtherscanContract
from etherscan.client import Client
from etherscan.accounts import Account

from src.utils.misc_utils import w3_infura
from web3 import Web3


def init_contract(address: str):

    address = Web3.toChecksumAddress(address)
    contract_abi = EtherscanContract(
        address=address, api_key=os.environ["ETHERSCAN_API_KEY"]
    ).get_abi()
    contract = w3_infura.eth.contract(address=address, abi=contract_abi)
    return contract


class EtherscanContractExtended(Account):
    def __init__(self, address=Client.dao_address, api_key="YourApiKey"):
        Account.__init__(self, address=address, api_key=api_key)
        self.url_dict[self.MODULE] = "account"

    def get_tx_with(
        self, addr: str, start_block: int = 0, end_block: int = -1, sort="asc"
    ):

        self.url_dict[self.ACTION] = "txlist"
        self.url_dict[self.SORT] = sort
        self.url_dict[self.START_BLOCK] = str(start_block)
        end_block = str(end_block)
        if int(end_block) == -1:
            end_block = "latest"
        self.url_dict[self.END_BLOCK] = end_block
        self.build_url()
        req = self.connect()
        relevant_txes = []
        for tx in req["result"]:
            if tx["from"] in [addr, addr.lower(), Web3.toChecksumAddress(addr)]:
                relevant_txes.append(tx)

        return relevant_txes


def address_is_contract(address: str) -> bool:
    return w3_infura.eth.getCode(address) > HexBytes(0)
