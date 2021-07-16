from marshmallow_dataclass import dataclass

from src.core.datastructures.defaults import DefaultVal
from src.core.datastructures.defaults import NoneRefersDefault


@dataclass
class PoolFees(NoneRefersDefault):

    accrued_fees: float = DefaultVal(0)
    block_start: int = DefaultVal(0)
    block_end: int = DefaultVal(0)
