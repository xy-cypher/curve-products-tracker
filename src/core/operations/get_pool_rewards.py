from typing import List

from brownie import network

from src.core.datastructures.rewards import Rewards
from src.core.products_factory import Product
from src.utils.contract_utils import init_contract


class OutstandingRewardsCalculator:
    def __init__(
        self,
        product: Product,
    ):

        self.pool_contract = init_contract(product.contract.addr)

        # initialise pool token contracts
        if len(product.token_contracts.items()) != 1:
            raise  # there should only be 1 token contract
        self.pool_token_contract = {}
        for token_name, info in product.token_contracts.items():
            token_contract = init_contract(info.addr)
            self.pool_token_contract = {
                "contract": token_contract,
                "decimals": token_contract.decimals(),
            }

        # get num underlying tokens
        self.num_underlying_tokens = 0
        for i in range(100):
            try:
                self.pool_contract.coins(i)
                self.num_underlying_tokens += 1
            except ValueError:  # max index reached, hence count is num tokens
                break

        # initialise auxiliary contracts:
        # NOTE: gauge tokens have the same decimals as lp tokens
        self.gauge_contracts = {}
        for contract_name, contract in product.other_contracts.items():

            contract_name: str = contract_name
            gauge_contract = None
            decimals = None
            if contract.addr:
                gauge_contract = init_contract(contract.addr)
                decimals = self.pool_token_contract["decimals"]

            gauge = {"contract": gauge_contract, "decimals": decimals}

            self.gauge_contracts[contract_name] = gauge

    def get_outstanding_rewards(self, address: str) -> List[Rewards]:

        curve_rewards = self.get_curve_rewards(address=address)
        convex_rewards = self.get_convex_rewards(address=address)
        pool_rewards = self.get_pool_rewards(address=address)

        return [pool_rewards, curve_rewards, convex_rewards]

    def get_curve_rewards(self, address: str):
        return Rewards()

    def get_convex_rewards(self, address: str):
        return Rewards()

    def get_pool_rewards(self, address: str):
        return Rewards()
