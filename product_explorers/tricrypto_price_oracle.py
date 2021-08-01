import json

from src.core.operations.get_position_multicall import (
    CurvePositionCalculatorMultiCall,
)
from src.core.operations.get_user_lp_tokens import (
    get_liquidity_positions_for_participants,
)
from src.core.products_factory import TRICRYPTO_V2
from src.utils.network_utils import connect


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

        tricrypto_price_oracle = tricrypto_calculator.get_oracle_prices_dict()


if __name__ == "__main__":
    main()
