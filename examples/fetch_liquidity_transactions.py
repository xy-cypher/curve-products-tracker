import argparse
import sys

from src.core.operations.get_liquidity_transaction import (
    get_liquidity_moved_for_tx,
)


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="Get added or removed liquidity in transaction."
    )
    parser.add_argument(
        dest="tx_hash",
        help="transaction hash",
        type=str,
    )
    return parser.parse_args(args)


def main(args):
    """
    example txes:
    added liquidity:
        1. 0xc77884d3af1782869772f57ecfadd62cc16087e0576092928eaaec4ada9bbfb3
        2. 0xcc1695bab2ff8343e5b407aae3a97ea4ec37d9b5f4cb88847752eefaebfd0181

    remove_liquidity:
        1. 0x30fbbe236793dbb0538b0ad0751f99cb54b472ee399542903f5f0db2623bfa0f

    remove_liquidity_one_coin:
        1. 0x7d6a9f9365544c4abf889765b749c984b9e5e1632bafe2665229feec61b0b6a8
    """
    import json

    args = parse_args(args)
    print(f"Tx hash: {args.tx_hash}")

    liquidity_tx = get_liquidity_moved_for_tx(args.tx_hash)
    print(json.dumps(liquidity_tx.__dict__, indent=4, default=str))


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
