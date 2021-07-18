from datetime import datetime
from typing import Optional
from typing import Tuple

import pytz
from brownie import network
from brownie import ZERO_ADDRESS
from brownie.network import transaction

from src.core.datastructures.pool_transactions import LiquidityTransaction
from src.core.datastructures.tokens import Token
from src.utils.coin_prices import get_historical_price_coingecko
from src.utils.contract_utils import init_contract


def get_added_liquidity_for_tx(tx_hash: str, currency: str = "usd"):

    network.connect("mainnet")

    tx_receipt = transaction.TransactionReceipt(tx_hash)
    date = pytz.utc.localize(datetime.utcfromtimestamp(tx_receipt.timestamp))

    minted_lp_tokens = get_minted_tokens(tx_receipt.events)
    added_tokens = get_added_tokens(tx_receipt.events)

    token_objects = []
    pool_contract = init_contract(tx_receipt.receiver)
    for index, num_tokens in enumerate(added_tokens):

        token_address = pool_contract.coins(index)
        token_contract = init_contract(token_address)
        token_name = token_contract.name()

        coingecko_price = get_historical_price_coingecko(
            token_contract=token_contract,
            query_datetime=date,
            currency=currency,
        )

        value_tokens = (
            num_tokens / 10 ** token_contract.decimals()
        ) * coingecko_price.quote

        token_objects.append(
            Token(
                name=token_name,
                address=token_address,
                num_tokens=num_tokens,
                coingecko_price=coingecko_price,
                value_tokens=value_tokens,
            )
        )

    return LiquidityTransaction(
        date=date,
        contract_function=tx_receipt.fn_name,
        transaction_hash=tx_hash,
        lp_tokens=minted_lp_tokens,
        block_number=tx_receipt.block_number,
        transaction_fees_eth=tx_receipt.gas_used
        * 1e-18
        * tx_receipt.gas_price,
        tokens=token_objects,
    )


def get_minted_tokens(events: Optional[network.event.EventDict]) -> int:

    for event in events:
        if "_from" in event.keys() and event["_from"] == ZERO_ADDRESS:
            minted_tokens = event["_value"]  # ZERO_ADDRESS mints lp tokens
            return minted_tokens
    return 0


def get_added_tokens(events: Optional[network.event.EventDict]) -> Tuple:

    for event in events:
        if event.name == "AddLiquidity":
            tokens_added = event["token_amounts"]
            return tokens_added
