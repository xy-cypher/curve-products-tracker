import argparse
from typing import Optional

from src.core.operations.get_position import CurvePositionCalculator
from src.core.products_factory import TRICRYPTO_V2


def parse_args():
    parser = argparse.ArgumentParser(
        description="Get TriCrypto positions and deposit info for address."
    )
    parser.add_argument(
        "--address",
        dest="address",
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
        "--block-number",
        dest="block_number",
        help="Block at which to calculate position.",
        type=Optional[int],
        default=None,
    )
    return parser.parse_args()


def main():
    import json
    from brownie._config import CONFIG
    from brownie import network
    from brownie import web3

    args = parse_args()

    # if block_number is empty, then set it to latest block
    block_number = args.block_number
    if not block_number:
        block_number = web3.eth.block_number

    # change network provider to user specified
    CONFIG.networks["mainnet"]["host"] = args.node_provider_https
    CONFIG.networks["mainnet"]["name"] = "Ethereum mainnet"

    # connect to mainnet
    network.connect("mainnet")

    print(f"User Address: {args.address}")
    print("Fetching all deposits to Curve v2 TriCrypto pool.")

    tricrypto_calculator = CurvePositionCalculator(TRICRYPTO_V2)
    current_position = tricrypto_calculator.get_current_position(
        args.address, block_number=block_number
    )
    print(json.dumps(current_position.__dict__, indent=4, default=str))

    # disconnect
    network.disconnect()


if __name__ == "__main__":
    main()
