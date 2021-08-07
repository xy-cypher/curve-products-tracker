from brownie.network.contract import Contract

from src.utils.network_utils import connect

connect(
    "https://eth-mainnet.alchemyapi.io/v2/AxU0de70ONfvbD-3_pQX0wUlaBK6g3G4"
)

offending_contract = Contract.from_explorer(
    "0xDeFd8FdD20e0f34115C7018CCfb655796F6B2168"
)
offending_address = "0x155ddac174dc33a1c7054b90ae8c31228776d147"

offending_block = 12821248

print(
    offending_contract.balanceOf(offending_address, block_identifier=12821248)
)
