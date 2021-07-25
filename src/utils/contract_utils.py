from brownie import network
from brownie.network.contract import Contract
from brownie.network.contract import ContractNotFound
from etherscan.accounts import Account
from etherscan.client import Client
from hexbytes import HexBytes
from web3 import Web3
from web3.exceptions import InvalidAddress

from src.utils.misc_utils import w3_infura


def init_contract(address: str):

    if not address_is_contract(address):
        raise ContractNotFound

    try:
        contract = Contract(address_or_alias=address)
    except InvalidAddress:
        raise
    except Exception as e:
        print(e)
        contract = Contract.from_explorer(address=address)

    return contract


class TransactionScraper(Account):
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
