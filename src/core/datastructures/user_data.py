from dataclasses import dataclass
from typing import Optional

from src.core.datastructures.current_position import CurrentPosition
from src.core.datastructures.defaults import NoneRefersDefault
from src.core.datastructures.pool_transactions import HistoricalTransactions


@dataclass
class UserData(NoneRefersDefault):

    address: str
    current_position: Optional[CurrentPosition]
    historical_liquidity_transactions: Optional[HistoricalTransactions]
