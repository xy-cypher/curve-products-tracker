from web3.exceptions import ABIEventFunctionNotFound, MismatchedABI

from src.utils.constants import TRICRYPTO_LP_TOKEN_ADDR
from src.utils.exceptions import IncorrectContractException

from web3.types import TxReceipt


def get_minted_lp_tokens_deposit_contract(tx_receipt: TxReceipt) -> int:
    """If liquidity is added via contract address
    0x72b40Caa258c237c6F5947E291650808B913e9fC. An example of a transaction
    is 0xd557732dc9c2065140ddfe75c7b7dae8a4b9aaa95e628f199ed4938a1350b769.

    The 3rd log, or log[2], is the sub-call to the minter
    0x0000000000000000000000000000000000000000 which mints lp tokens and sends
    it to to the Curve CyptoSwap Deposit Zap contract
    0x331aF2E331bd619DefAa5DAc6c038f53FCF9F785. An example event log:

    https://etherscan.io/tx/0xd557732dc9c2065140ddfe75c7b7dae8a4b9aaa95e628f199ed4938a1350b769#eventlog

    :param tx_receipt:
    :return: minted_lp_tokens: int
    """
    log_to_process = tx_receipt["logs"][2]
    try:
        processed_log = TRICRYPTO_LP_TOKEN_ADDR.events.Transfer().processLog(log_to_process)
    except Exception as e:
        raise IncorrectContractException
    minted_lp_tokens = processed_log["args"]["_value"]
    return minted_lp_tokens


def get_minted_lp_tokens_pool_contract(tx_receipt: TxReceipt) -> int:
    """If liquidity is added via contract address
    0x80466c64868E1ab14a1Ddf27A676C3fcBE638Fe5. An example of a transaction
    is 0xcc1695bab2ff8343e5b407aae3a97ea4ec37d9b5f4cb88847752eefaebfd0181.

    The 2nd log, or log[1], is the sub-call to the minter
    0x0000000000000000000000000000000000000000 hich mints lp tokens and sends
    it to the user, thereafter followed by the last transaction in the last log
    which adds liquidity to the pool. An example event log:

    https://etherscan.io/tx/0xcc1695bab2ff8343e5b407aae3a97ea4ec37d9b5f4cb88847752eefaebfd0181#eventlog

    :param tx_receipt:
    :return: minted_tokens: int
    """
    log_to_process = tx_receipt["logs"][1]
    try:
        processed_log = TRICRYPTO_LP_TOKEN_ADDR.events.Transfer().processLog(log_to_process)
    except (ABIEventFunctionNotFound, MismatchedABI):
        raise IncorrectContractException
    minted_lp_tokens = processed_log["args"]["_value"]
    return minted_lp_tokens
