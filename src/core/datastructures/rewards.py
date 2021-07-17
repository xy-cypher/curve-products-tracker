from dataclasses import field
from datetime import datetime
from typing import List

import pytz as pytz
from marshmallow_dataclass import dataclass

from src.core.datastructures.base import BaseDataStruct
from src.core.datastructures.coingecko_price import CoinGeckoPrice
from src.core.datastructures.tokens import Token


@dataclass
class Rewards(BaseDataStruct):

    tokens: List[Token] = field(default_factory=lambda: [Token()])


@dataclass
class ClaimedReward(BaseDataStruct):

    date: datetime = pytz.utc.localize(datetime.utcnow())
    rewards: Rewards = Rewards()


@dataclass
class OutstandingRewards(BaseDataStruct):

    coingecko_price: CoinGeckoPrice = CoinGeckoPrice()
    token: str = ""
    num_tokens: float = 0
    value_tokens: float = 0
