import argparse

from src.utils.contract_utils import get_all_txes
from src.utils.network_utils import connect


def parse_args():

    parser = argparse.ArgumentParser(
        description="Get current Pool Liquidity Providers."
    )
    parser.add_argument(
        "--pool_address",
        dest="pool_address",
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

    historical_txes = get_all_txes(
        from_block=args.from_block, address=args.pool_address
    )

    participating_addrs = set([i["from"] for i in historical_txes])

    print("Total num participants in pool history: ", len(participating_addrs))
    print("\n".join(participating_addrs))


if __name__ == "__main__":
    main()
