import json

from datetime import datetime
import pytz
from typing import Union

from web3.types import TxData, TxReceipt
from hexbytes import HexBytes

from eth_typing import Hash32, HexStr

from src.utils.misc_utils import w3_infura, to_dict


class Transaction:

    def __init__(self, transaction_hash: Union[str, Hash32, HexBytes, HexStr]):
        """Etherscan transaction class

        :param transaction_hash: dict derived from Etherscan API
        """
        self.tx_hash = transaction_hash
        self.tx_data: TxData = w3_infura.eth.get_transaction(self.tx_hash)
        block_details = w3_infura.eth.get_block(self.tx_data.blockNumber)
        self.tx_datetime = pytz.utc.localize(
            datetime.utcfromtimestamp(block_details.timestamp)
        )

        self.from_address = self.tx_data["from"]
        self.to_address = self.tx_data["to"]

        # tx logs:
        self.tx_receipt: TxReceipt = w3_infura.eth.get_transaction_receipt(self.tx_hash)

    @property
    def __parsed_dict__(self):
        return to_dict(self.__dict__)

    @property
    def __json__(self):
        return json.dumps(self.__parsed_dict__, indent=4, sort_keys=True, default=str)


def main():
    tx_hash_str = "0xc77884d3af1782869772f57ecfadd62cc16087e0576092928eaaec4ada9bbfb3"
    parsed_tx = Transaction(tx_hash_str)
    print(parsed_tx.__json__)


if __name__ == "__main__":
    main()
