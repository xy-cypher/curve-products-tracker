import datetime
from typing import List
from typing import Optional

from marshmallow_dataclass import dataclass

from src.core.datastructures.defaults import DefaultVal
from src.core.datastructures.defaults import NoneRefersDefault
from src.core.datastructures.rewards import ClaimedReward
from src.core.datastructures.tokens import Token


@dataclass
class LiquidityTransactions(NoneRefersDefault):

    date: datetime.datetime = DefaultVal(datetime.utcnow())
    contract_function: str = DefaultVal("")
    transaction_hash: str = DefaultVal("")
    lp_tokens: float = DefaultVal(0)
    block_number: int = DefaultVal(0)
    transaction_fees_eth: float = DefaultVal(0)
    tokens: List[Token] = DefaultVal([Token()])


@dataclass
class HistoricalTransactions(NoneRefersDefault):

    claimed_rewards: List[ClaimedReward] = DefaultVal([ClaimedReward()])
    liquidity_transactions: LiquidityTransactions = DefaultVal(
        LiquidityTransactions()
    )
