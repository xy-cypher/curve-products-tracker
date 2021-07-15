from dataclasses import dataclass

from src.core.datastructures.coingecko_price import CoinGeckoPrice


@dataclass
class Token:

    token: str
    num_tokens: float
    value_tokens: float
    coingecko_price: CoinGeckoPrice
