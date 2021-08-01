from typing import List

import brownie

from src.core.sanity_check.check_value import is_dust


def get_lp_tokens_of_users(
    participating_addrs: List, staking_contracts: List, block_identifier: int
):
    active_user_balance = {}
    for staking_contract in staking_contracts:
        if not staking_contract:
            continue

        with brownie.multicall(address=staking_contract.address):
            balances = [
                staking_contract.balanceOf(
                    addr, block_identifier=block_identifier
                )
                for addr in participating_addrs
            ]
            user_balance = dict(zip(participating_addrs, balances))
        active_user_balance[staking_contract.address] = user_balance

    # get all participants with non-zero balances in any of the three
    # pools
    active_participants = active_user_balance[
        list(active_user_balance.keys())[0]
    ].keys()

    active_balances = {}
    for addr in active_participants:
        user_balance = {}
        for pool_addr in active_user_balance.keys():
            user_balance_in_pool = int(active_user_balance[pool_addr][addr])
            if user_balance_in_pool:
                user_balance[str(pool_addr)] = user_balance_in_pool
        if not is_dust(sum(user_balance.values()), token_decimal=18):
            active_balances[str(addr)] = user_balance

    return active_balances


def get_liquidity_positions_for_participants(participants_dict: dict):

    total_lp_tokens = {
        addr: sum(lp_tokens.values())
        for addr, lp_tokens in participants_dict.items()
    }

    return total_lp_tokens
