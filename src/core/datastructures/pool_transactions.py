from dataclasses import field
from datetime import datetime
from typing import List

import pytz as pytz
from marshmallow_dataclass import dataclass

from src.core.datastructures.base import BaseDataStruct
from src.core.datastructures.rewards import ClaimedReward
from src.core.datastructures.tokens import Token


@dataclass
class LiquidityTransactions(BaseDataStruct):

    date: datetime = pytz.utc.localize(datetime.utcnow())
    contract_function: str = ""
    transaction_hash: str = ""
    lp_tokens: float = 0
    block_number: int = 0
    transaction_fees_eth: float = 0
    tokens: List[Token] = field(default_factory=lambda: [Token()])


@dataclass
class HistoricalTransactions(BaseDataStruct):

    claimed_rewards: List[ClaimedReward] = field(
        default_factory=lambda: [ClaimedReward()]
    )
    liquidity_transactions: LiquidityTransactions = LiquidityTransactions()
