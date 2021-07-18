import argparse
import sys

from src.core.operations.get_added_liquidity import get_added_liquidity_for_tx


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Get added liquidity in transaction hash."
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
    added liquidity: 0xc77884d3af1782869772f57ecfadd62cc16087e0576092928eaaec4ada9bbfb3
    """
    import json

    args = parse_args(args)
    print(f"Tx hash: {args.tx_hash}")

    added_liquidity = get_added_liquidity_for_tx(args.tx_hash)
    print(json.dumps(added_liquidity.__dict__, indent=4, default=str))


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
