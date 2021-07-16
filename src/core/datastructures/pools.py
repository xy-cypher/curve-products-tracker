from dataclasses import field
from typing import List

from marshmallow_dataclass import dataclass

from src.core.datastructures.base import BaseDataStruct
from src.core.datastructures.current_position import CurrentPosition


@dataclass
class Pool(BaseDataStruct):

    name: str = ""
    contract_address: str = ""
    current_position: CurrentPosition = CurrentPosition()


@dataclass
class Pools(BaseDataStruct):

    pool: List[Pool] = field(default_factory=lambda: [Pool()])
