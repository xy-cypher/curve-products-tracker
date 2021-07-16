from typing import List
from typing import Optional

from marshmallow_dataclass import dataclass

from src.core.datastructures.current_position import CurrentPosition
from src.core.datastructures.defaults import DefaultVal
from src.core.datastructures.defaults import NoneRefersDefault


@dataclass
class Pool(NoneRefersDefault):

    name: str = DefaultVal("")
    contract_address: str = DefaultVal("")
    current_position: CurrentPosition = DefaultVal(CurrentPosition())


@dataclass
class Pools(NoneRefersDefault):

    pool: List[Pool] = DefaultVal([Pool()])
