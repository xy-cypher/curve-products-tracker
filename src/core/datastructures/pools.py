from typing import List
from typing import Optional

from marshmallow_dataclass import dataclass

from src.core.datastructures.current_position import CurrentPosition
from src.core.datastructures.defaults import NoneRefersDefault


@dataclass
class Pool(NoneRefersDefault):

    name: str
    contract_address: str
    current_position: Optional[CurrentPosition]


@dataclass
class Pools(NoneRefersDefault):

    pool: List[Pool]
