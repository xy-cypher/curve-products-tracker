import argparse
import json

import brownie

from src.core.sanity_check.check_value import is_dust
from src.utils.contract_utils import get_all_txes
from src.utils.contract_utils import init_contract
from src.utils.network_utils import connect


def parse_args():

    parser = argparse.ArgumentParser(
        description="Get current Pool Liquidity Providers."
    )
    parser.add_argument(
        "--pool-token-address",
        dest="pool_token_address",
        help="Address to fetch info for.",
        type=str,
    )
    parser.add_argument(
        "--convex-gauge-address",
        dest="convex_gauge_addr",
        help="Address to fetch info for.",
        type=str,
    )
    parser.add_argument(
        "--curve-gauge-address",
        dest="curve_gauge_addr",
        help="Address to fetch info for.",
        type=str,
    )
    parser.add_argument(
        "--node-provider-https",
        dest="node_provider_https",
        help="Node provider API. It must have Archive Node access (Alchemy). "
        "Go to: https://alchemy.com/?r=0f41076514343f84 to get $100 of "
        "credits. They also have a free tier with archival node access. "
        "After you make an account, you can fetch your api key and enter "
        "it in this parameter, "
        "e.g. https://eth-mainnet.alchemyapi.io/v2/API_KEY",
        type=str,
    )
    parser.add_argument(
        "--from-block",
        dest="from_block",
        type=int,
        default=100,
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # connect to custom note provider in args
    connect(args.node_provider_https)

    pool_token_contract = init_contract(args.pool_token_address)
    gauge_contract_convex = init_contract(args.convex_gauge_addr)
    gauge_contract_curve = init_contract(args.curve_gauge_addr)

    current_block = brownie.web3.eth.block_number

    # todo: implement for pool token that is not using etherscan (limited to previous 10000 entries)
    historical_txes = get_all_txes(
        start_block=args.from_block,
        end_block=current_block,
        address=pool_token_contract.address,
    )

    participating_addrs = set([i["from"] for i in historical_txes])

    participating_user_balance = {}
    for staking_contract in [
        pool_token_contract,
        gauge_contract_convex,
        gauge_contract_curve,
    ]:
        if not staking_contract:
            continue

        with brownie.multicall(
            address=staking_contract.address, block_identifier=current_block
        ):
            balances = [
                staking_contract.balanceOf(addr)
                for addr in participating_addrs
            ]
            user_balance = dict(zip(participating_addrs, balances))
        participating_user_balance[staking_contract.address] = user_balance

    # get all participants with non-zero balances in any of the three pools
    active_participants = participating_user_balance[
        list(participating_user_balance.keys())[0]
    ].keys()
    active_balances = {}
    for addr in active_participants:
        user_balance = {}
        for pool_addr in participating_user_balance.keys():
            user_balance_in_pool = int(
                participating_user_balance[pool_addr][addr]
            )
            if user_balance_in_pool:
                user_balance[str(pool_addr)] = user_balance_in_pool
        if not is_dust(sum(user_balance.values()), token_decimal=18):
            active_balances[str(addr)] = user_balance

    active_balances_block = {current_block: active_balances}

    print("Total num participants in pool history: ", len(active_balances))
    with open("../data/pool_participants.json", "w") as f:
        json.dump(active_balances_block, f, indent=4)


if __name__ == "__main__":
    main()
