import datetime
from dataclasses import dataclass
from typing import List
from typing import Optional

from src.core.datastructures.defaults import NoneRefersDefault
from src.core.datastructures.rewards import ClaimedReward
from src.core.datastructures.tokens import Token


@dataclass
class LiquidityTransactions(NoneRefersDefault):

    date: datetime.datetime
    contract_function: str
    transaction_hash: str
    lp_tokens: float
    block_number: int
    transaction_fees_eth: float
    tokens: List[Token]


@dataclass
class HistoricalTransactions(NoneRefersDefault):

    claimed_rewards: List[ClaimedReward]
    liquidity_transactions: Optional[LiquidityTransactions]
