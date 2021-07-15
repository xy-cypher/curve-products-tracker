from dataclasses import dataclass


@dataclass
class PoolFees:

    accrued_fees: float
    block_start: int
    block_end: int
