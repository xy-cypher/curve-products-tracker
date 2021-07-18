from marshmallow_dataclass import dataclass

from src.core.datastructures.base import BaseDataStruct
from src.core.datastructures.coin_price import CoinPrice


@dataclass
class Token(BaseDataStruct):

    name: str = ""
    address: str = ""
    num_tokens: float = 0
    value_tokens: float = 0
    coingecko_price: CoinPrice = CoinPrice()
