from datetime import datetime
from datetime import timedelta
from time import sleep
from typing import Union

import pytz
from brownie import network
from pycoingecko import CoinGeckoAPI

from src.core.datastructures.coin_price import CoinPrice
from src.utils.constants import SUSHISWAP_ROUTER_CONTRACT
from src.utils.constants import USDT_ADDR
from src.utils.contract_utils import init_contract

COINGECKO = CoinGeckoAPI()


def get_sushiswap_price(
    token_in: str,
    token_out: str,
    num_tokens: int,
    block_number: Union[str, int],
):

    # TODO: get historical swap quotes by block number using sushiswap router
    was_connected_to_mainnet = network.show_active() == "mainnet"
    if block_number != "latest" and network.show_active() != "archivenode":
        network.connect("archivenode")

    sushiswap_router = init_contract(SUSHISWAP_ROUTER_CONTRACT)
    amounts_out = sushiswap_router.getAmountsOut(
        int(num_tokens), [token_in, token_out]
    ).call()

    if was_connected_to_mainnet and network.show_active() != "mainnet":
        network.connect("mainnet")

    return amounts_out


def get_current_price_coingecko(
    token_name: str, currency: str = "usd"
) -> CoinPrice:

    token_price = COINGECKO.get_price(ids=id, vs_currencies=currency)

    return CoinPrice(
        time=pytz.utc.localize(datetime.utcnow()),
        currency=currency,
        quote=token_price[token_name][currency],
    )


def get_historical_price_coingecko(
    token_contract: str, query_datetime: datetime, currency: str = "usd"
) -> CoinPrice:

    from_timestamp = query_datetime.timestamp()

    response: dict = {"prices": [], "market_caps": [], "total_volumes": []}
    add_minutes = 60
    while not response["prices"]:
        to_timestamp = (
            query_datetime + timedelta(minutes=add_minutes)
        ).timestamp()
        response = (
            COINGECKO.get_coin_market_chart_range_from_contract_address_by_id(
                id="ethereum",
                contract_address=token_contract,
                vs_currency=currency,
                from_timestamp=int(from_timestamp),
                to_timestamp=int(to_timestamp),
            )
        )
        if response["prices"]:
            break
        print("Warning: Coingecko Rate Limit might get breached.")
        add_minutes += 1
        sleep(0.5)  # can't make too many calls to CoinGecko ...

    response_price = response["prices"][0][1]
    response_date = pytz.utc.localize(datetime.utcfromtimestamp(to_timestamp))

    return CoinPrice(
        time=response_date, currency=currency, quote=response_price
    )


def main():
    import json

    query_datetime = datetime.utcnow() - timedelta(days=10)
    fetched_prices = get_historical_price_coingecko(
        token_contract="0xdAC17F958D2ee523a2206206994597C13D831ec7",
        query_datetime=query_datetime,
        currency="usd",
    )
    print(json.dumps(fetched_prices, indent=4, default=str))


if __name__ == "__main__":
    main()