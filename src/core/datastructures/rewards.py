from dataclasses import dataclass
from typing import List

from src.core.datastructures.coingecko_price import CoinGeckoPrice
from src.core.datastructures.tokens import Token


@dataclass
class Rewards:

    tokens: List[Token]


@dataclass
class ClaimedRewards:
    rewards: List[Rewards]


@dataclass
class OutstandingRewards:

    token: str
    num_tokens: float
    value_tokens_usd: float
    coingecko_price: CoinGeckoPrice
