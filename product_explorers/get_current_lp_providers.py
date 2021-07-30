import argparse
import json
import logging
import os
import time

import brownie
from etherscan.client import EmptyResponse

from src.core.sanity_check.check_value import is_dust
from src.utils.contract_utils import get_all_txes
from src.utils.contract_utils import init_contract
from src.utils.network_utils import connect


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s,%(msecs)d-4s %(levelname)-4s [%(filename)s %(module)s:%(lineno)d] :: %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
)


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
    parser.add_argument(
        "--sleep-time-seconds",
        dest="sleep_time_seconds",
        type=int,
        default=60,
    )
    parser.add_argument(
        "--cache-filename",
        dest="cache_filename",
        type=str,
        default="../data/pool_participants.json",
    )
    return parser.parse_args()


def load_cached_positions(cache_filename: str):

    with open(cache_filename, "r") as f:
        cached_positions = json.load(f)

    return cached_positions


def cache_positions(active_balances_block: dict, cache_filename: str):
    # todo: maybe use a redis cache instead of saving it
    with open(cache_filename, "w") as f:
        json.dump(active_balances_block, f, indent=4)


def main():
    args = parse_args()

    # connect to custom note provider in args
    logging.info("Connecting to Node Provider ...")
    connect(args.node_provider_https)
    logging.info("... connected!")

    logging.info("Initialising pool and gauge contracts ...")
    pool_token_contract = init_contract(args.pool_token_address)
    gauge_contract_convex = init_contract(args.convex_gauge_addr)
    gauge_contract_curve = init_contract(args.curve_gauge_addr)
    logging.info("... initialised!")

    from_block = args.from_block
    cached_positions = {}
    block_in_cache = "None"
    if os.path.exists(args.cache_filename):
        logging.info(
            "Cached positions exist. Loading block number of last query."
        )
        cached_positions = load_cached_positions(args.cache_filename)
        block_in_cache = list(cached_positions.keys())[0]
        from_block = int(block_in_cache)

    while True:

        logging.info("Awake.")

        if not brownie.network.is_connected():

            connect(args.node_provider_https)

        current_block = brownie.web3.eth.block_number
        logging.info(f"Current block: {current_block}")
        logging.info(f"Fetching Etherscan Txes from block {from_block} ...")

        try:

            historical_txes = get_all_txes(
                start_block=from_block - 6006000,
                end_block=current_block,
                address=pool_token_contract.address,
            )

        except EmptyResponse:

            if cached_positions:
                logging.info(
                    f"No transactions since {from_block}. Positions did not "
                    f"change. Modifying cache block number and re-cacheing."
                )

                from_block = current_block
                modified_cache = {
                    current_block: cached_positions[block_in_cache]
                }
                cache_positions(modified_cache, args.cache_filename)

            # adjust from_block to current_block
            from_block = current_block

            logging.info("Disconnecting Brownie")
            brownie.network.disconnect()

            logging.info(f"Sleeping for {args.sleep_time_seconds} seconds.")
            time.sleep(args.sleep_time_seconds)

            continue

        logging.info(
            f"... done! Number of transactions: {len(historical_txes)}"
        )

        participating_addrs = set([i["from"] for i in historical_txes])
        if cached_positions:
            participating_addrs.update(cached_positions[block_in_cache].keys())

        logging.info(f"Number of unique addresses: {len(participating_addrs)}")
        logging.info("Fetching balances ...")
        active_user_balance = {}
        for staking_contract in [
            pool_token_contract,
            gauge_contract_convex,
            gauge_contract_curve,
        ]:
            if not staking_contract:
                continue

            with brownie.multicall(
                address=staking_contract.address,
                block_identifier=current_block,
            ):
                balances = [
                    staking_contract.balanceOf(addr)
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
                user_balance_in_pool = int(
                    active_user_balance[pool_addr][addr]
                )
                if user_balance_in_pool:
                    user_balance[str(pool_addr)] = user_balance_in_pool
            if not is_dust(sum(user_balance.values()), token_decimal=18):
                active_balances[str(addr)] = user_balance

        active_balances_block = {current_block: active_balances}

        logging.info(
            f"Total num participants in pool history: {len(active_balances)}"
        )
        logging.info("Cacheing data ...")
        cache_positions(active_balances_block, args.cache_filename)

        # adjust from_block to current_block
        from_block = current_block

        logging.info("Disconnecting Brownie")
        brownie.network.disconnect()

        logging.info(f"Sleeping for {args.sleep_time_seconds} seconds.")
        time.sleep(args.sleep_time_seconds)


if __name__ == "__main__":
    main()
