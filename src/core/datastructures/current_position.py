from dataclasses import field
from datetime import datetime
from typing import List

import pytz as pytz
from marshmallow_dataclass import dataclass

from src.core.datastructures.base import BaseDataStruct
from src.core.datastructures.fees import PoolFees
from src.core.datastructures.rewards import OutstandingRewards
from src.core.datastructures.tokens import Token


@dataclass
class CurrentPosition(BaseDataStruct):

    time: datetime = pytz.utc.localize(datetime.utcnow())
    lp_tokens: float = 0
    curve_gauge_tokens: float = 0
    convex_gauge_tokens: float = 0
    accrued_fees: PoolFees = PoolFees()
    tokens: List[Token] = field(default_factory=lambda: [Token()])
    outstanding_rewards: OutstandingRewards = OutstandingRewards()
