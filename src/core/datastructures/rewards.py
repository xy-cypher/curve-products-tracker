from dataclasses import dataclass
from datetime import datetime
from typing import List

from src.core.datastructures.coingecko_price import CoinGeckoPrice
from src.core.datastructures.defaults import NoneRefersDefault
from src.core.datastructures.tokens import Token


@dataclass
class Rewards(NoneRefersDefault):

    tokens: List[Token]


@dataclass
class ClaimedReward(NoneRefersDefault):

    date: datetime.datetime
    rewards: Rewards


@dataclass
class OutstandingRewards(NoneRefersDefault):

    coingecko_price: CoinGeckoPrice
    token: str = ""
    num_tokens: float = 0
    value_tokens: float = 0

    def null(self):
        coingecko_price: CoinGeckoPrice
        token: str = ""
        num_tokens: float = 0
        value_tokens: float = 0
