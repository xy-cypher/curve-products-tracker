import os

from etherscan.contracts import Contract as EtherscanContract
from web3 import Web3

from etherscan.client import Client
from etherscan.accounts import Account


w3_infura = Web3(
    Web3.HTTPProvider(
        f"https://mainnet.infura.io/v3/{os.environ['WEB3_INFURA_PROJECT_ID']}"
    )
)


def to_dict(dict_to_parse: dict):
    # convert any 'AttributeDict' type found to 'dict'

    parsed_dict = dict(dict_to_parse)
    for key, val in parsed_dict.items():
        if 'list' in str(type(val)):
            parsed_dict[key] = [parse_value(x) for x in val]
        else:
            parsed_dict[key] = parse_value(val)
    return parsed_dict


def parse_value(val):
    # check for nested dict structures to iterate through
    if 'dict' in str(type(val)).lower():
        parsed_val = {}
        for key, _val in val.items():
            if 'list' in str(type(_val)).lower():
                parsed_val[key] = [parse_value(x) for x in _val]
                continue
            parsed_val[key] = parse_value(_val)
        return parsed_val
    # convert 'HexBytes' type to 'str'
    elif 'HexBytes' in str(type(val)):
        return val.hex()
    else:
        return val


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
