from typing import List

from brownie import network

from src.core.curve_contracts_factory import PoolInfo
from src.core.datastructures.rewards import Rewards
from src.utils.contract_utils import init_contract


class OutstandingRewardsCalculator:
    def __init__(
        self,
        pool_info: PoolInfo,
        network_name: str = "mainnet",
    ):
        network.connect(network_name)

        self.curve_gauge_contract = init_contract(
            pool_info.curve_gauge_contract
        )

        # TODO: Remove this later as it is temporary code.
        self.convex_gauge_contract = None
        if pool_info.convex_gauge_contract:
            self.convex_gauge_contract = init_contract(
                pool_info.convex_gauge_contract
            )

        self.pool_contract = init_contract(pool_info.pool_contract)
        self.pool_token_contract = init_contract(pool_info.pool_token_contract)
        self.pool_token_decimals = self.pool_token_contract.decimals()

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


