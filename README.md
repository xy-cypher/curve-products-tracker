PROTOTYPE PROJECT TO MAKE A PROOF-OF-WORK THAT WILL BE IN PRODUCTION.

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).
# Curve TriCrypto Position Tracker

Tricrypto Position Tracker is a tool that allows a liquidity provider in [Curve's new v2 liquidity pool for US Dollar (Tether; USDT), Wrapped Bitcoin (WBTC) and Ether (ETH)](https://curve.fi/tricrypto) on the Ethereum blockchain. This tool enables monitoring one's liquidity pool positions.

### Available Functionality
1. Get current position in TriCrypto pool.
2. Get deposits.

### In progress
1. App using python-flask and React.js

### Planned
3. Deployed stack in the interwebs
4. Get value of tokens when deposited.
5. Get removed liquidity and value of tokens when withdrawn.

### Holy Grail
**Historical LP positions** (will work with Archival nodes, but not enough experience there yet).

## Installation

There are a few packages to install in order to run the scripts in this repository. The user also needs API keys from [Etherscan](https://etherscan.io/apis) and [Infura](https://infura.io/) in order to query the blockchain for transactions and infer positions.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements in this repository. The user is encouraged to use virtual environments. The instructions here are tested on a 2021 Mac M1 Air.

Requirements: Python >= 3.6.0

```bash
# create virtual environment first
cd api
python3 -m venv venv

# activate virtual environment
source ./venv/bin/activate

# update pip
python3 -m pip install --upgrade pip

# install requirements
pip install -r ../requirements.txt
```

## Python friendly scripts:
After installation, a user can run the following scrip:

```shell
python tricrypto_tracker.py <user_address>
```
This will return a json string as follows:
```json
{
    "added_liquidity": {
        "02 July, 2021 13:29:01 ": {
            "tokens": {
                "USDT": 165199.7462105,
                "WBTC": 0.0,
                "ETH": 0.0
            },
            "coingecko_token_price": {
                "WBTC": 33621.056636124435,
                "ETH": 2121.657900633364,
                "USDT": 1.0016307604207397
            },
            "token_value": {
                "USDT": 165469.14741813633,
                "WBTC": 0.0,
                "ETH": 0.0
            },
            "block_number": "12748469",
            "gas_price_eth": 8e-09,
            "transaction_fees": 0.002302592
        }
    },
    "current_position": {
        "07 July, 2021 13:44:35 ": {
            "USDT": {
                "token_contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                "curve_oracle_price_usd": 1,
                "num_tokens": 1738993.311167,
                "value_tokens_usd": 1738993.311167,
                "coingecko_price_usd": 1.0
            },
            "WBTC": {
                "token_contract_address": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
                "curve_oracle_price_usd": 34717.28246217235,
                "num_tokens": 50.17445831,
                "value_tokens_usd": 1741920.8415347605,
                "coingecko_price_usd": 34791
            },
            "ETH": {
                "token_contract_address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                "curve_oracle_price_usd": 2375.356016704667,
                "num_tokens": 730.4234639654944,
                "value_tokens_usd": 1735015.7698727017,
                "coingecko_price_usd": 2382.41
            }
        }
    }
}
```

## Available Scripts for local deployment

In the project directory, you can run:

To run the project, you need 2 terminals
1. `yarn start` starts the React.js frontend.
2. `yarn start-api` starts the flask backend.

### `yarn start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `yarn start-api`

Runs the back-end flask api.\
Open [http://localhost:5000](http://localhost:5000) to use it.

Examples:
`http://localhost:5000/summary/0x2B99d34a2d45cFBF5B9d5d7595F28fD786AE61c7`

As you develop, the back-end also changes. If there are erroneous requests, you can see this in the terminal logs.

### `yarn test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `yarn build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `yarn eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.
