from dataclasses import dataclass
from typing import List

from src.core.datastructures.fees import PoolFees
from src.core.datastructures.tokens import Token


@dataclass
class CurrentPosition:

    lp_tokens: float
    accrued_fees: PoolFees
    tokens: List[Token]
