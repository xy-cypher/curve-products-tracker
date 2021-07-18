from marshmallow_dataclass import dataclass

from src.core.datastructures.base import BaseDataStruct


CURVE_CRYPTOSWAP_ADDR = "0x331aF2E331bd619DefAa5DAc6c038f53FCF9F785"


@dataclass
class PoolInfo(BaseDataStruct):

    pool_contract: str = ""
    pool_token_contract: str = ""
    curve_gauge_contract: str = ""
    convex_gauge_contract: str = ""
    cryptoswap_contract: str = CURVE_CRYPTOSWAP_ADDR


TRICRYPTO_V2_POOL = PoolInfo(
    pool_contract="0xD51a44d3FaE010294C616388b506AcdA1bfAAE46",
    pool_token_contract="0xc4AD29ba4B3c580e6D59105FFf484999997675Ff",
    curve_gauge_contract="0xDeFd8FdD20e0f34115C7018CCfb655796F6B2168",
    convex_gauge_contract="",
)

TRICRYPTO_V1_POOL = PoolInfo(
    pool_contract="0x80466c64868E1ab14a1Ddf27A676C3fcBE638Fe5",
    pool_token_contract="0xcA3d75aC011BF5aD07a98d02f18225F9bD9A6BDF",
    curve_gauge_contract="0x6955a55416a06839309018A8B0cB72c4DDC11f15",
    convex_gauge_contract="0x5Edced358e6C0B435D53CC30fbE6f5f0833F404F",
)
