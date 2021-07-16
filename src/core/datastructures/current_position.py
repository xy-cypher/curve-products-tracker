from datetime import datetime
from typing import List
from typing import Optional

from marshmallow_dataclass import dataclass

from src.core.datastructures.defaults import DefaultVal
from src.core.datastructures.defaults import NoneRefersDefault
from src.core.datastructures.fees import PoolFees
from src.core.datastructures.rewards import OutstandingRewards
from src.core.datastructures.tokens import Token


@dataclass
class CurrentPosition(NoneRefersDefault):

    time: datetime = DefaultVal(datetime.utcnow())
    lp_tokens: float = DefaultVal(0)
    gauge_tokens: float = DefaultVal(0)
    accrued_fees: PoolFees = DefaultVal(PoolFees())
    tokens: List[Token] = DefaultVal([Token()])
    outstanding_rewards: OutstandingRewards = DefaultVal(OutstandingRewards())
