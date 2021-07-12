from web3 import Web3
from web3.types import LogReceipt

from src.utils.contract_utils import init_contract
from src.utils.misc_utils import parse_value


class SubContractEvent:
    def __init__(
        self,
        contract_address: str,
        contract_name: str,
        event_name: str,
    ):

        if not Web3.isChecksumAddress(contract_address):
            contract_address = Web3.toChecksumAddress(contract_address)

        self.contract = init_contract(address=contract_address)
        self.contract_name = contract_name
        self.event_name = event_name

        # set event
        self.event = self.__set_event()

    def __set_event(self):

        for event in self.contract.events.__iter__():
            if event.event_name == self.event_name:
                return event

    def process_log(self, log: LogReceipt) -> dict:
        event_data = self.event().processLog(log)
        dict_event_data = parse_value(event_data)
        dict_event_data["contract_name"] = self.contract_name
        return dict_event_data


def main():
    import json
    from src.core.transaction import Transaction

    # This is an example of add_liquidity method of the Curve CryptoSwap
    # Deposit Zap contract 0x331aF2E331bd619DefAa5DAc6c038f53FCF9F785 .
    # The add_liquidity method mints the LP tokens in the 2nd event of the
    # contract. The contract that orchestrates this event is the Curve LP
    # Base Contract with the address
    # 0xcA3d75aC011BF5aD07a98d02f18225F9bD9A6BDF. The method used is
    # Transfer().
    tx_hash_str = "0xd557732dc9c2065140ddfe75c7b7dae8a4b9aaa95e628f199ed4938a1350b769"
    parsed_tx = Transaction(tx_hash_str)
    event_log_to_process = parsed_tx.tx_receipt["logs"][2]
    orchestrating_contract_address = "0xcA3d75aC011BF5aD07a98d02f18225F9bD9A6BDF"
    event_name = "Transfer"
    contract_name = "curve_base_lp_token"

    sub_contract_event = SubContractEvent(
        contract_address=orchestrating_contract_address,
        contract_name=contract_name,
        event_name=event_name,
    )

    processed_log = sub_contract_event.process_log(event_log_to_process)
    print(json.dumps(processed_log, indent=4, sort_keys=True, default=str))

    # Example for removing liquidity
    tx_hash_str = "0x30fbbe236793dbb0538b0ad0751f99cb54b472ee399542903f5f0db2623bfa0f"
    parsed_tx = Transaction(tx_hash_str)
    event_log_to_process = parsed_tx.tx_receipt["logs"][4]
    orchestrating_contract_address = "0x80466c64868E1ab14a1Ddf27A676C3fcBE638Fe5"
    event_name = "RemoveLiquidity"
    contract_name = "tricrypto_lp"

    sub_contract_event = SubContractEvent(
        contract_address=orchestrating_contract_address,
        contract_name=contract_name,
        event_name=event_name,
    )

    processed_log = sub_contract_event.process_log(event_log_to_process)
    print(json.dumps(processed_log, indent=4, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
