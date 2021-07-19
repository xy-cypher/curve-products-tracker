from dataclasses import field
from typing import Dict

from marshmallow_dataclass import dataclass

from src.core.contracts_factory import ContractInfo
from src.core.contracts_factory import CRV3CRYPTO
from src.core.contracts_factory import TRICRYPTO_V2_CURVE_GAUGE
from src.core.contracts_factory import TRICRYPTO_V2_POOL
from src.core.datastructures.base import BaseDataStruct


@dataclass
class LiquidityPoolProduct(BaseDataStruct):

    product_name: str = ""
    pool_contract: ContractInfo = ContractInfo()
    pool_token_contract: ContractInfo = ContractInfo()
    other_contracts: Dict[str, ContractInfo] = field(
        default_factory=lambda: {"": ContractInfo()}
    )


TRICRYPTO_V2 = LiquidityPoolProduct(
    pool_contract=TRICRYPTO_V2_POOL,
    pool_token_contract=CRV3CRYPTO,
    other_contracts={
        "curve_gauge": TRICRYPTO_V2_CURVE_GAUGE,
        "convex_gauge": ContractInfo(),  # No contracts yet
    },
)
