from dataclasses import dataclass


@dataclass
class CoinGeckoPrice:

    currency: str
    quote: float
