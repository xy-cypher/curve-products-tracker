import argparse
import json

from src.core.operations.get_position_multicall import (
    CurvePositionCalculatorMultiCall,
)
from src.core.operations.get_user_lp_tokens import (
    get_liquidity_positions_for_participants,
)
from src.core.products_factory import TRICRYPTO_V2
from src.utils.network_utils import connect


def parse_args():
    parser = argparse.ArgumentParser(
        description="Get TriCrypto positions and deposit info for address."
    )
    parser.add_argument(
        "--pool-participants-file",
        dest="pool_participants_file",
        help="JSON file of all pool participants",
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
        "--block-steps",
        dest="block_steps",
        help="How many blocks to skip between each query",
        type=int,
        default=1,
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # connect to custom note provider in args
    connect(args.node_provider_https)

    # initialise tricrypto calculator
    tricrypto_calculator = CurvePositionCalculatorMultiCall(TRICRYPTO_V2)

    # get all liquidity providers
    with open(args.pool_participants_file, "r") as f:
        liquidity_providers = json.load(f)

    block_positions = {}
    for block_id in liquidity_providers.keys():
        aggregated_positions = get_liquidity_positions_for_participants(
            liquidity_providers[block_id]
        )
        block_position = tricrypto_calculator.get_position(
            lp_balances=aggregated_positions, block_identifier=int(block_id)
        )
        block_positions[int(block_id)] = block_position

    with open("../data/pool_participants_positions.json", "w") as f:
        json.dump(block_positions, f, indent=4)


if __name__ == "__main__":
    main()
