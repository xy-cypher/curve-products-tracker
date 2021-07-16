from datetime import datetime
from typing import List

from marshmallow_dataclass import dataclass

from src.core.datastructures.coingecko_price import CoinGeckoPrice
from src.core.datastructures.defaults import DefaultVal
from src.core.datastructures.defaults import NoneRefersDefault
from src.core.datastructures.tokens import Token


@dataclass
class Rewards(NoneRefersDefault):

    tokens: List[Token] = DefaultVal([Token()])


@dataclass
class ClaimedReward(NoneRefersDefault):

    date: datetime.datetime = DefaultVal(datetime.utcnow())
    rewards: Rewards = DefaultVal(Rewards())


@dataclass
class OutstandingRewards(NoneRefersDefault):

    coingecko_price: CoinGeckoPrice
    token: str = ""
    num_tokens: float = 0
    value_tokens: float = 0
