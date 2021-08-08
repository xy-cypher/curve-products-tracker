import argparse
import logging
import os
import time
from datetime import datetime

import brownie.network
from brownie.network.contract import Contract
from eth_abi.exceptions import InsufficientDataBytes

from src.core.operations.get_position_multicall import (
    CurvePositionCalculatorMultiCall,
)
from src.core.operations.get_user_lp_tokens import (
    get_liquidity_positions_for_participants,
)
from src.core.operations.get_user_lp_tokens import get_lp_tokens_of_users
from src.core.products_factory import TRICRYPTO_V2
from src.utils.cache_utils import cache_object_to_json
from src.utils.contract_utils import get_all_txes
from src.utils.network_utils import connect


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s,%(msecs)d-4s %(levelname)-4s [%(filename)s %(module)s:%(lineno)d] :: %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
)

SLEEP_TIME = 1800


def parse_args():

    parser = argparse.ArgumentParser(
        description="Get current Pool Liquidity Providers."
    )
    parser.add_argument(
        "--cache-dir",
        dest="cache_dir",
        type=str,
        default="../data/block_positions",
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
        "--block-steps",
        dest="block_steps",
        type=int,
        default=1000,
    )
    return parser.parse_args()


def main():

    args = parse_args()

    # connect to custom note provider in args
    connect(args.node_provider_https)

    staking_contracts = [
        Contract(TRICRYPTO_V2.token_contracts["crv3crypto"].addr),
        Contract(TRICRYPTO_V2.other_contracts["curve_gauge"].addr),
        Contract(TRICRYPTO_V2.other_contracts["convex_gauge"].addr),
    ]

    # initialise tricrypto
    tricrypto_calculator = CurvePositionCalculatorMultiCall(TRICRYPTO_V2)
    from_block = TRICRYPTO_V2.contract.genesis_block

    steps = args.block_steps
    to_block = from_block + steps  # initialisation
    extra_steps_if_error = 100
    sleep_time = 1

    while True:

        # get block number (this uses a free api). can do with brownie but
        # why rpc call when you can avoid it?
        current_block = brownie.chain.height
        logging.info(f"Current block: {current_block}")

        # set longer sleep time if reached current block
        if to_block > current_block:
            logging.info(f"Reached max block height {current_block}")
            to_block = current_block
            sleep_time = SLEEP_TIME  # longer sleep time.

        # get addresses of active participants
        logging.info(f"Fetching Txes between {from_block} : {current_block}")
        historical_txes = get_all_txes(
            address=TRICRYPTO_V2.token_contracts["crv3crypto"].addr,
        )
        logging.info(f"... done! Num lp token txes: {len(historical_txes)}")
        from_addresses = [i["from"] for i in historical_txes]
        to_addresses = [i["to"] for i in historical_txes]
        all_addreses = from_addresses + to_addresses
        all_unique_participants = list(set(all_addreses))

        # remove zero addr
        current_liquidity_providers = list(
            filter(None, all_unique_participants)
        )

        # connect to brownie if not connected
        if not brownie.network.is_connected():
            connect(args.node_provider_https)

        # get active balances
        logging.info("Fetching active balances")
        while True:

            try:

                active_balances = get_lp_tokens_of_users(
                    participating_addrs=current_liquidity_providers,
                    staking_contracts=staking_contracts,
                    block_identifier=to_block,
                )
                break

            except InsufficientDataBytes:

                logging.warning(
                    f"InsufficientDataBytes encountered: "
                    f"retrying with {extra_steps_if_error} block steps ahead"
                )
                to_block = to_block + steps + extra_steps_if_error

                continue

        # aggregate positions to get total lp tokens
        logging.info("aggregating positions")
        aggregated_positions = get_liquidity_positions_for_participants(
            active_balances
        )

        # get block positions
        logging.info("calculating underlying tokens")
        start_time = datetime.now()
        block_position = tricrypto_calculator.get_position(
            lp_balances=aggregated_positions, block_identifier=to_block
        )
        logging.info(f"time taken: {datetime.now() - start_time}")

        # cache positions for block
        logging.info("cacheing output")
        cache_filename = os.path.join(args.cache_dir, f"{to_block}.json")
        cache_object_to_json(obj=block_position, cache_filename=cache_filename)

        # disconnect_brownie
        brownie.network.disconnect()

        # all steps succeeded! we can step up now
        to_block = to_block + steps

        logging.info(f"sleeping for {sleep_time} seconds \n")
        time.sleep(sleep_time)


if __name__ == "__main__":
    main()
