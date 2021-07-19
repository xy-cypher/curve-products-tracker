import argparse
import sys

from src.core.operations.get_current_position import CurrentPositionCalculator
from src.core.products_factory import TRICRYPTO_V2


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="Get TriCrypto positions and deposit info for address."
    )
    parser.add_argument(
        dest="address",
        help="Address to fetch info for.",
        type=str,
    )
    return parser.parse_args(args)


def main(args):
    import json

    args = parse_args(args)
    print(f"User Address: {args.address}")
    print("Fetching all deposits to Curve v2 TriCrypto pool.")

    tricrypto_calculator = CurrentPositionCalculator(TRICRYPTO_V2)
    current_position = tricrypto_calculator.get_current_position(args.address)
    print(json.dumps(current_position.__dict__, indent=4, default=str))


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
