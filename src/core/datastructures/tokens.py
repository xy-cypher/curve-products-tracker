from marshmallow_dataclass import dataclass

from src.core.datastructures.coingecko_price import CoinGeckoPrice
from src.core.datastructures.defaults import DefaultVal
from src.core.datastructures.defaults import NoneRefersDefault


@dataclass
class Token(NoneRefersDefault):

    token: str = DefaultVal("")
    num_tokens: float = DefaultVal(0)
    value_tokens: float = DefaultVal(0)
    coingecko_price: CoinGeckoPrice = DefaultVal(CoinGeckoPrice())
