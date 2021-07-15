from brownie import network
from brownie.network.contract import Contract
from brownie.network.transaction import ContractNotFound
from brownie.network.transaction import TransactionNotFound
from brownie.network.transaction import TransactionReceipt

from src.curve_contract_factory.crv_tri_crypto.constants import TRICRYPTO_CONVEX_GAUGE
from src.curve_contract_factory.crv_tri_crypto.constants import TRICRYPTO_CURVE_GAUGE
from src.curve_contract_factory.crv_tri_crypto.constants import TRICRYPTO_POOL_CONTRACT


class CurrentPositionParser:
    def __init__(self, network_name: str = "mainnet"):

        if not network.is_connected():
            network.connect(network_name)

        self.curve_gauge_contracts = Contract.from_explorer(TRICRYPTO_CURVE_GAUGE)
        self.convex_gauge_contracts = Contract.from_explorer(TRICRYPTO_CONVEX_GAUGE)
        self.pool_contract = Contract.from_explorer(TRICRYPTO_POOL_CONTRACT)

    def parse_transaction(self, tx_hash: str):

        pass
