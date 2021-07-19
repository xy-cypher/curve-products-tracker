from marshmallow_dataclass import dataclass

from src.core.datastructures.base import BaseDataStruct


@dataclass
class ContractInfo(BaseDataStruct):
    contract_name: str = ""
    contract_addr: str = ""


# MISC CONTRACTS

CURVE_CRYPTOSWAP = ContractInfo(
    contract_name="Curve CryptoSwap",
    contract_addr="0x331aF2E331bd619DefAa5DAc6c038f53FCF9F785",
)

CONVEX_TOKEN = ContractInfo(
    contract_name="Convex Token",
    contract_addr="0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B",
)

CURVE_TOKEN = ContractInfo(
    contract_name="Curve DAO Token",
    contract_addr="0xD533a949740bb3306d119CC777fa900bA034cd52",
)

cvxCRV_REWARDS = ContractInfo(
    contract_name="cvxCRV Rewards",
    contract_addr="0x3Fe65692bfCD0e6CF84cB1E7d24108E434A7587e",
)

CVX_REWARDS = ContractInfo(
    contract_name="CVX Rewards",
    contract_addr="0xCF50b810E57Ac33B91dCF525C6ddd9881B139332",
)


# 3POOL

_3CRV = ContractInfo(
    contract_name="3crv",
    contract_addr="0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490",
)


# TRICRYPTO_V2

TRICRYPTO_V2_POOL = ContractInfo(
    contract_name="TriCrypto v2 Pool",
    contract_addr="0xD51a44d3FaE010294C616388b506AcdA1bfAAE46",
)

CRV3CRYPTO = ContractInfo(
    contract_name="crv3crypto",
    contract_addr="0xc4AD29ba4B3c580e6D59105FFf484999997675Ff",
)

TRICRYPTO_V2_CURVE_GAUGE = ContractInfo(
    contract_name="TriCrypto v2 Curve Gauge",
    contract_addr="0xDeFd8FdD20e0f34115C7018CCfb655796F6B2168",
)
