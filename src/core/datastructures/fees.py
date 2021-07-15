from marshmallow_dataclass import dataclass

from src.core.datastructures.defaults import NoneRefersDefault


@dataclass
class PoolFees(NoneRefersDefault):

    accrued_fees: float
    block_start: int
    block_end: int
