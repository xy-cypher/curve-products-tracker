from marshmallow_dataclass import dataclass

from src.core.datastructures.defaults import NoneRefersDefault


@dataclass
class CoinGeckoPrice(NoneRefersDefault):

    currency: str = ""
    quote: float = 0
