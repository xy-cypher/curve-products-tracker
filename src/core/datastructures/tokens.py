from marshmallow_dataclass import dataclass

from src.core.datastructures.coingecko_price import CoinGeckoPrice
from src.core.datastructures.defaults import NoneRefersDefault


@dataclass
class Token(NoneRefersDefault):

    token: str
    num_tokens: float
    value_tokens: float
    coingecko_price: CoinGeckoPrice
