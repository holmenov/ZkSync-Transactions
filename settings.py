"""
----------------------------------------MAIN SETTINGS------------------------------------------

    MAX_GAS - 40 | Gwei Control. Maximum value of GWEI in Ethereum for software operation.

    GAS_MULTIPLAYER = 0.8 | Multiplier for MAX_GAS value.

    RANDOM_WALLETS - True | Take the wallets in random order.

    REMOVE_WALLET - True | To delete wallets after work or not. (IF NOT - SET FALSE).

    USE_PROXY - True | Use proxy or not.

    START_PERIOD = [1, 600] | The time period in which the wallets will be run.
        For example, wallets will be launched with a timer from 1 to 600 seconds after software launch.
            The first value is from, the second is to.
    
    REPEATS_PER_WALLET = 5 | The number of repetitions of each module.
    
    SLEEP_AFTER_WORK = [10, 30] | Sleeps after each module. A random number between 10 and 30 is selected.
    
    SLIPPAGE = 5 | Slippage in % for swaps.
    
    LANDINGS_SLEEP = [90, 300] | Sleep spacing for landing protocols. That's how long it will hold the money and withdraw after that time has elapsed.
    
    CUSTOM_ROUTES_MODULES = [                                       |   With custom routes modules you can make your own routes.
        ['deposit_eraland'],                                        |   One line - one transaction.
        ['swap_syncswap'],                                          |   You can specify any number of functions on each line.
        ['wrap_eth'],                                               |   The software will select a random function in the list.
        ['send_mail', 'rubyscore_vote', 'owlto_checkin'],
        ['increase_allowance', 'approve', 'transfer', None]
    ]
    
---------------------------------------FUNCTIONS NAME------------------------------------------

    swap_syncswap           |   Swap on SyncSwap.
    swap_woofi              |   Swap on WooFi.
    deposit_eraland         |   Supply (Redeem) EraLand.
    wrap_eth                |   Wrap (Unwrap) $ETH.
    send_mail               |   Send mail via DMail.
    increase_allowance      |   Increase Allowance to random address.
    approve                 |   Approve to random address.
    transfer                |   Transfer to random address.
    rubyscore_vote          |   Vote on RubyScore.
    owlto_checkin           |   Daily check in on OwlTo.

-----------------------------------------------------------------------------------------------
"""

class MainSettings:
    MAX_GAS = 100

    GAS_MULTIPLAYER = 0.8

    RANDOM_WALLETS = True

    REMOVE_WALLET = True

    USE_PROXY = True

    START_PERIOD = [1, 10]
    
    REPEATS_PER_WALLET = 1

    SLEEP_AFTER_WORK = [10, 30]

    SLIPPAGE = 5
    
    LANDINGS_SLEEP = [90, 300]

    CUSTOM_ROUTES_MODULES = [
        ['send_mail', 'increase_allowance', 'approve', 'transfer', 'rubyscore_vote', 'owlto_checkin']
    ]

    # CUSTOM_ROUTES_MODULES = [
    #     ['deposit_eraland'],
    #     ['swap_syncswap'],
    #     ['wrap_eth'],
    #     ['send_mail', 'rubyscore_vote', 'owlto_checkin'],
    #     ['increase_allowance', 'approve', 'transfer', None]
    # ]

"""
----------------------------------------OKX WITHDRAW------------------------------------------

    SYMBOL = 'ETH'              |   Data for withdraw from OKX.
    CHAIN = 'zkSync Era'        |   You can find this data on OKX.
    FEE = 0.00015               |   https://www.okx.com/balance/withdrawal

    AMOUNT = [0.006, 0.008]     |   Amount from and amount to withdrawal.
    
    BALANCE_TOP_UP = 0.01       |   Minimum balance for top up balance (Only for $ETH).
    
    SECRET_KEY = 'YOUR_DATA'    |   Get your API data here:
    API_KEY = 'YOUR_DATA'       |   https://www.okx.com/account/my-api
    PASSPHRASE = 'YOUR_DATA'    |   Paste your secret, api keys and passphrase.

----------------------------------------------------------------------------------------------
"""

class OKXSettings:
    SYMBOL = 'ETH'
    CHAIN = 'zkSync Era'
    FEE = 0.00015

    AMOUNT_WITHDRAW = [0.006, 0.008]

    BALANCE_TOP_UP = 0.01

    SECRET_KEY = 'YOUR_DATA'
    API_KEY = 'YOUR_DATA'
    PASSPHRASE = 'YOUR_DATA'

"""
--------------------------------------------------MODULE SETTINGS--------------------------------------------------

    Each module has its own individual settings. Each module is labeled with the class "Module_Name".
    
    AMOUNT = [0.00035, 0.00065]     |   Amount for transactions. A random number in the interval will be used.
    
    DECIMAL = 5                     |   Decimal places for rounding for a random transaction amount.
    
    FROM_TOKEN = 'ETH'              |   Tokens for swaps.
    TO_TOKEN = 'USDC'               |   In this example, we swap $ETH to $USDC.
    
    USE_PERCENTS = False            |   Use % of balance
    
    PERCENTS = [3, 7]               |   How much % to use?
    
    SWAP_REVERSE = True             |   Doing a reverse swap for the same amount?
    
    WITHDRAW = True                 |   To withdraw liquidity from landing protocols or not.
    
    TOKENS = ['USDT', 'USDC']       |   Tokens list for work. You can choose one or several tokens.
    
    NFT_ADDRESS = ''                |   Paste NFT Contract address. Works only for free NFT with mint() func.

-------------------------------------------------------------------------------------------------------------------
"""

class ModulesSettings:
    
    class EraLend:
        AMOUNT = [0.0005, 0.0009]
        DECIMAL = 5
        
        USE_PERCENTS = False
        PERCENTS = [3, 7]
        
        WITHDRAW = True

    class SyncSwap:
        FROM_TOKEN = 'ETH'
        TO_TOKEN = 'USDC'
        
        AMOUNT = [0.0005, 0.0009]
        DECIMAL = 5
        
        USE_PERCENTS = False
        PERCENTS = [3, 7]
        
        SWAP_REVERSE = True
    
    class WooFi:
        FROM_TOKEN = 'ETH'
        TO_TOKEN = 'USDC'
        
        AMOUNT = [0.0005, 0.0009]
        DECIMAL = 5
        
        USE_PERCENTS = False
        PERCENTS = [3, 7]
        
        SWAP_REVERSE = True

    class WrapETH:
        AMOUNT = [0.0005, 0.0009]
        DECIMAL = 5
        
        USE_PERCENTS = False
        PERCENTS = [3, 7]
        
        UNWRAP_ETH = True
    
    class Tokens:

        class IncreaseAllowance: # ETH not avaliable
            TOKENS = ['USDT', 'USDC', 'DAI', 'WETH', 'WBTC', 'UNI']

            AMOUNT = [0.000025, 0.000045]
            DECIMAL = 7
        
        class Approve: # ETH not avaliable
            TOKENS = ['USDT', 'USDC', 'DAI', 'WETH', 'WBTC', 'UNI']

            AMOUNT = [0.000025, 0.000045]
            DECIMAL = 7

        class Transfer:
            TOKENS = ['ETH']

            AMOUNT = [0.000025, 0.000045]
            DECIMAL = 7

    class MintNFT:
        NFT_ADDRESS = ''