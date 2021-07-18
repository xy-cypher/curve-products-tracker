import argparse
import sys

from src.core.curve_contracts_factory import TRICRYPTO_V2_POOL
from src.core.operations.get_current_position import CurrentPositionCalculator


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
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
    """Wrapper allowing :funcs:`added_liquidity` and `get_tricrypto_liquidity_positions`
    to be called with string arguments in a CLI fashion.

    It prints the result to the ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["0x331aF2E331bd619DefAa5DAc6c038f53FCF9F785"]``).
    """
    import json

    args = parse_args(args)
    print(f"User Address: {args.address}")
    print("Fetching all deposits to Curve v2 TriCrypto pool.")

    tricrypto_calculator = CurrentPositionCalculator(TRICRYPTO_V2_POOL)
    current_position = tricrypto_calculator.get_current_position(args.address)
    print(json.dumps(current_position.__dict__, indent=4, default=str))


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m ${qual_pkg}.skeleton 42
    #
    run()
