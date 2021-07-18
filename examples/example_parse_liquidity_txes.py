import json

from src.core.contract_transaction import ContractTransaction
from src.core.curve_contracts_factory import (
    TRICRYPTO_LP_TOKEN,
)
from src.core.curve_contracts_factory import (
    TRICRYPTO_POOL_CONTRACT,
)
from src.core.method_event import SubContractEvent
from src.core.transaction import Transaction


def main():

    # The 'add_liquidity' event for which log needs to get processed
    add_liquidity_event = SubContractEvent(
        contract_address=TRICRYPTO_LP_TOKEN.address,
        contract_name="curve_base_lp_token",
        event_name="Transfer",
    )

    # The 'remove_liquidity' event for which log needs to get processed
    remove_liquidity_event = SubContractEvent(
        contract_address=TRICRYPTO_POOL_CONTRACT.address,
        contract_name="tricrypto_lp",
        event_name="RemoveLiquidity",
    )

    # The 'remove_liquidity_one' event for which log needs to get processed
    remove_liquidity_one_event = SubContractEvent(
        contract_address=TRICRYPTO_POOL_CONTRACT.address,
        contract_name="tricrypto_lp",
        event_name="RemoveLiquidityOne",
    )

    # Example 1

    # interacting with Curve CryptoSwap contract 0x331af2e331bd619defaa5dac6c038f53fcf9f785.
    # There are 6 sub-contract calls:
    # 1. WETH9 Contract 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 deposits
    #    0 WETH to Curve CryptoSwap
    # 2. TetherToken contract 0xdAC17F958D2ee523a2206206994597C13D831ec7 orchestrates
    #    transfer from user address 0x7a16fF8270133F063aAb6C9977183D9e72835428 to
    #    Curve CryptoSwap contract.
    # 3. TetherToken transfer orchestrates transfer between Curve CryptoSwap to
    #    TriCrypto Liquidity Pool contract 0x80466c64868E1ab14a1Ddf27A676C3fcBE638Fe5
    # 4. Curve LP Token base implementation contract 0xcA3d75aC011BF5aD07a98d02f18225F9bD9A6BDF
    #    orchestrates minting of LP tokens from ZERO ADDRESS to Curve CryptoSwap contract
    # 5. TriCrypto LP Contract adds liquidity on behalf of the Curve CryptoSwap contract
    # 6. Curve LP token base implementation contract orchestrates minted LP token transfer from
    #    Curve CryptoSwap to user address.

    tx_hash_str = (
        "0xc77884d3af1782869772f57ecfadd62cc16087e0576092928eaaec4ada9bbfb3"
    )
    parsed_tx = Transaction(tx_hash_str)

    contract_tx_parser = ContractTransaction(
        contract_address=parsed_tx.tx_data.to,
    )

    parsed_tx = contract_tx_parser.parse_transaction(
        tx_hash=tx_hash_str,
        sub_contract_event=add_liquidity_event,
    )

    print(json.dumps(parsed_tx, indent=4))

    # Example 2
    tx_hash_str = (
        "0xcc1695bab2ff8343e5b407aae3a97ea4ec37d9b5f4cb88847752eefaebfd0181"
    )
    parsed_tx = Transaction(tx_hash_str)

    contract_tx_parser = ContractTransaction(
        contract_address=parsed_tx.tx_data.to,
    )

    parsed_tx = contract_tx_parser.parse_transaction(
        tx_hash=tx_hash_str,
        sub_contract_event=add_liquidity_event,
    )

    print(json.dumps(parsed_tx, indent=4))

    # Example 3 - Remove Liquidity in all three coins
    tx_hash_str = (
        "0x30fbbe236793dbb0538b0ad0751f99cb54b472ee399542903f5f0db2623bfa0f"
    )
    parsed_tx = Transaction(tx_hash_str)

    contract_tx_parser = ContractTransaction(
        contract_address=parsed_tx.tx_data.to,
    )

    parsed_tx = contract_tx_parser.parse_transaction(
        tx_hash=tx_hash_str,
        sub_contract_event=remove_liquidity_event,
    )

    print(json.dumps(parsed_tx, indent=4))

    # Example 4 - Remove Liquidity in one coin
    tx_hash_str = (
        "0x7d6a9f9365544c4abf889765b749c984b9e5e1632bafe2665229feec61b0b6a8"
    )
    parsed_tx = Transaction(tx_hash_str)

    contract_tx_parser = ContractTransaction(
        contract_address=parsed_tx.tx_data.to,
    )

    parsed_tx = contract_tx_parser.parse_transaction(
        tx_hash=tx_hash_str,
        sub_contract_event=remove_liquidity_one_event,
    )

    print(json.dumps(parsed_tx, indent=4))


if __name__ == "__main__":
    main()
