from typing import Optional

from marshmallow_dataclass import dataclass

from src.core.datastructures.current_position import CurrentPosition
from src.core.datastructures.defaults import DefaultVal
from src.core.datastructures.defaults import NoneRefersDefault
from src.core.datastructures.pool_transactions import HistoricalTransactions


@dataclass
class UserData(NoneRefersDefault):

    address: str = DefaultVal("")
    current_position: CurrentPosition = DefaultVal(CurrentPosition())
    historical_liquidity_transactions: HistoricalTransactions = DefaultVal(
        HistoricalTransactions()
    )
