import os
from typing import List

import requests as requests
from brownie import ZERO_ADDRESS


def get_mint_or_burn_txs(
    user_address: str, token_addr: str, from_block: int, tx_type: str = "mint"
) -> List:

    from_addr = ZERO_ADDRESS
    to_addr = user_address
    if tx_type == "burn":
        from_addr = user_address
        to_addr = ZERO_ADDRESS

    tx_lp_tokens = requests.post(
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
                    "fromAddress": from_addr,
                    "toAddress": to_addr,
                    "contractAddresses": [token_addr],
                    "category": ["external", "token"],
                }
            ],
        },
    )

    lp_txes = tx_lp_tokens.json()["result"]["transfers"]

    return lp_txes
