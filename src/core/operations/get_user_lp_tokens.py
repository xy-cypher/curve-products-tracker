import json


def get_liquidity_positions_for_participants(participants_dict: dict):

    total_lp_tokens = {
        addr: sum(lp_tokens.values())
        for addr, lp_tokens in participants_dict.items()
    }

    return total_lp_tokens


def main():
    import os

    pool_participants_file = "../../../data/pool_participants.json"

    if not os.path.exists(pool_participants_file):
        pass

    with open(pool_participants_file, "r") as f:
        pool_participants = json.load(f)

    user_lp_tokens = get_liquidity_positions_for_participants(
        pool_participants
    )
    print(json.dumps(user_lp_tokens, indent=4))


if __name__ == "__main__":
    main()
