from dataclasses import dataclass
from typing import List
from typing import Optional

from src.core.datastructures.current_position import CurrentPosition


@dataclass
class Pool:

    name: str
    contract_address: str
    current_position: Optional[CurrentPosition]


@dataclass
class Pools:

    pool: List[Pool]
