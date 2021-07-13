from datetime import datetime
from datetime import timedelta
from time import sleep

from pycoingecko import CoinGeckoAPI

COINGECKO = CoinGeckoAPI()


def get_prices_of_coins(currency: str = "usd"):
    eth_price = COINGECKO.get_price(ids="ethereum", vs_currencies="usd")["ethereum"][
        currency
    ]
    wbtc_price = COINGECKO.get_price(ids="wrapped-bitcoin", vs_currencies="usd")[
        "wrapped-bitcoin"
    ][currency]
    usdt_price = COINGECKO.get_price(ids="tether", vs_currencies="usd")["tether"][
        currency
    ]
    return {
        currency: {"USDT": usdt_price, "WBTC": wbtc_price, "ETH": eth_price},
    }


def get_prices_of_coins_at(query_datetime: datetime, currency: str = "usd"):

    from_timestamp = query_datetime.timestamp()

    ids = {"USDT": "tether", "WBTC": "wrapped-bitcoin", "ETH": "ethereum"}
    prices = {}
    for ticker, id in ids.items():

        response: dict = {"prices": [], "market_caps": [], "total_volumes": []}
        add_minutes = 60
        while not response["prices"]:
            to_timestamp = (query_datetime + timedelta(minutes=add_minutes)).timestamp()
            response = COINGECKO.get_coin_market_chart_range_by_id(
                id=id,
                vs_currency=currency,
                from_timestamp=int(from_timestamp),
                to_timestamp=int(to_timestamp),
            )
            if response["prices"]:
                break
            print("Warning: Coingecko Rate Limit might get breached.")
            add_minutes += 1
            sleep(5)  # can't make too many calls to CoinGecko ...

        # do some processing here:
        response_prices = response["prices"][0][1]

        # compile prices:
        prices[ticker] = response_prices

    prices_in_currency = {currency: prices}

    return prices_in_currency


def main():
    import json

    query_datetime = datetime.utcnow() - timedelta(days=10)
    fetched_prices = get_prices_of_coins_at(
        query_datetime=query_datetime,
        currency="usd",
    )
    print(json.dumps(fetched_prices, indent=4))


if __name__ == "__main__":
    main()
