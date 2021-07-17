from marshmallow_dataclass import dataclass

from src.core.datastructures.base import BaseDataStruct
from src.core.datastructures.coingecko_price import CoinGeckoPrice


@dataclass
class Token(BaseDataStruct):

    token: str = ""
    num_tokens: float = 0
    value_tokens: float = 0
    coingecko_price: CoinGeckoPrice = CoinGeckoPrice()
