import os
from typing import List
from typing import Optional
from typing import Union

from brownie.network.contract import Contract
from etherscan.accounts import Account
from etherscan.client import Client
from web3 import Web3
from web3.exceptions import InvalidAddress


def init_contract(address: str) -> Contract:

    if not Web3.isAddress(address):
        return None

    try:
        contract = Contract(address_or_alias=address)
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

        return

    def get_tx(
        self,
        start_block: int = 0,
        end_block: Union[str, int] = "latest",
        sort: str = "asc",
    ):

        self.url_dict[self.ACTION] = "txlist"
        self.url_dict[self.SORT] = sort
        self.url_dict[self.START_BLOCK] = str(start_block)
        self.url_dict[self.END_BLOCK] = str(end_block)

        self.build_url()
        req = self.connect()

        return req["result"]


def get_all_txes(
    address: str, start_block: int = 0, end_block: Union[str, int] = "latest"
) -> List:

    tx_scraper = TransactionScraper(
        address=address, api_key=os.environ["ETHERSCAN_API_KEY"]
    )

    # todo: intervals should be segmented to 10000 block ranges
    txes = tx_scraper.get_tx(start_block=start_block, end_block=end_block)
    return txes
