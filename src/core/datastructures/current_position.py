from datetime import datetime
from typing import List
from typing import Optional

from marshmallow_dataclass import dataclass

from src.core.datastructures.defaults import NoneRefersDefault
from src.core.datastructures.fees import PoolFees
from src.core.datastructures.rewards import OutstandingRewards
from src.core.datastructures.tokens import Token


@dataclass
class CurrentPosition(NoneRefersDefault):

    time: datetime
    lp_tokens: float
    gauge_tokens: float
    accrued_fees: PoolFees
    tokens: List[Token]
    outstanding_rewards: Optional[OutstandingRewards]
