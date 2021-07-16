from marshmallow_dataclass import dataclass

from src.core.datastructures.defaults import DefaultVal
from src.core.datastructures.defaults import NoneRefersDefault


@dataclass
class CoinGeckoPrice(NoneRefersDefault):

    currency: str = DefaultVal("")
    quote: float = DefaultVal(0)
