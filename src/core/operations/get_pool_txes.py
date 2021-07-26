import os
from typing import List

import requests as requests
from brownie import ZERO_ADDRESS


def get_mint_txes(user_address: str, token_addr: str, from_block: int) -> List:

    minted_lp_tokens = requests.post(
        "https://eth-mainnet.alchemyapi.io/v2/"
        + os.environ["ALCHEMY_API_KEY"],
        json={
            "jsonrpc": "2.0",
            "id": 0,
            "method": "alchemy_getAssetTransfers",
            "params": [
                {
                    "fromBlock": hex(from_block),
                    "toBlock": "latest",
                    "fromAddress": ZERO_ADDRESS,
                    "toAddress": user_address,
                    "contractAddresses": [token_addr],
                    "category": ["external", "token"],
                }
            ],
        },
    )

    mint_txes = minted_lp_tokens.json()["result"]["transfers"]

    return mint_txes
