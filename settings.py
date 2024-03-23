"""
----------------------------------------MAIN SETTINGS------------------------------------------

    MAX_GAS - 40 | Gwei Control. Maximum value of GWEI in Ethereum for software operation.

    GAS_MULTIPLAYER = 0.8 | Multiplier for MAX_GAS value.

    RANDOM_WALLETS - True | Take the wallets in random order.

    EXCEL_PASSWORD = False | Use password on Excel file or not.

    USE_PROXY - True | Use proxy or not.

    START_PERIOD = [1, 600] | The time period in which the wallets will be run.
        For example, wallets will be launched with a timer from 1 to 600 seconds after software launch.
            The first value is from, the second is to.
    
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
    swap_inch               |   Swap on 1inch.
    swap_maverick           |   Swap on Maverick.
    swap_mute               |   Swap on Mute.
    swap_odos               |   Swap on Odos.
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

    EXCEL_PASSWORD = False

    USE_PROXY = True

    START_PERIOD = [1, 600]

    SLEEP_AFTER_WORK = [10, 30]

    SLIPPAGE = 5
    
    LANDINGS_SLEEP = [30, 90]

    CUSTOM_ROUTES_MODULES = [
        ['send_mail', 'owlto_checkin', 'wrap_eth'],
        ['approve', 'increase_allowance', 'rubyscore_vote', 'send_mail', 'wrap_eth'],
        ['swap_syncswap', 'swap_inch', 'swap_maverick', 'swap_mute', 'swap_odos'],
        ['approve', 'increase_allowance', 'rubyscore_vote', 'send_mail', 'wrap_eth'],
        ['send_mail', 'owlto_checkin', 'wrap_eth'],
        ['swap_syncswap', 'swap_inch', 'swap_maverick', 'swap_mute', 'swap_odos'],
        ['approve', 'increase_allowance', 'rubyscore_vote', 'send_mail', 'wrap_eth'],
        ['approve', 'increase_allowance', 'rubyscore_vote', 'send_mail', 'wrap_eth'],
    ]

"""
----------------------------------------OKX WITHDRAW------------------------------------------

    SYMBOL = 'ETH'                      |   Data for withdraw from OKX.
    CHAIN = 'zkSync Era'                |   You can find this data on OKX.
    FEE = 0.000041                      |   https://www.okx.com/balance/withdrawal

    AMOUNT = [0.006, 0.008]             |   Amount from and amount to withdrawal.
    
    BALANCE_TOP_UP = 0.01               |   Minimum balance for top up balance (Only for $ETH).
    
    WAIT_UNTIL_BALANCE_CREDITED = True  |   Wait until for tokens credited to move next modules.
    
    Get your API data here: https://www.okx.com/account/my-api
    Paste your secret, api keys and passphrase in wallets_data.xlsx.

----------------------------------------------------------------------------------------------
"""

class OKXSettings:
    SYMBOL = 'ETH'
    CHAIN = 'zkSync Era'
    FEE = 0.000041

    AMOUNT_WITHDRAW = [0.006, 0.008]

    BALANCE_TOP_UP = 0.01

    WAIT_UNTIL_BALANCE_CREDITED = True

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
    
    # For work get API-KEY: https://1inch.dev/portfolio-api/
    # Paste your api key in wallets_data.xlsx.
    class Inch:
        FROM_TOKEN = 'ETH'
        TO_TOKEN = 'USDC'
        
        AMOUNT = [0.0005, 0.0009]
        DECIMAL = 5
        
        USE_PERCENTS = False
        PERCENTS = [3, 7]
        
        SWAP_REVERSE = True
    
    class Maverick:
        FROM_TOKEN = 'ETH'
        TO_TOKEN = 'USDC'
        
        AMOUNT = [0.0005, 0.0009]
        DECIMAL = 5
        
        USE_PERCENTS = False
        PERCENTS = [3, 7]
        
        SWAP_REVERSE = True
        
    class Mute:
        FROM_TOKEN = 'ETH'
        TO_TOKEN = 'USDC'
        
        AMOUNT = [0.0005, 0.0009]
        DECIMAL = 5
        
        USE_PERCENTS = False
        PERCENTS = [3, 7]
        
        SWAP_REVERSE = True
    
    class Odos:
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

        # ETH Not avaliable.
        class IncreaseAllowance: 
            TOKENS = ['USDT', 'USDC', 'WETH', 'WBTC']

            AMOUNT = [0.000025, 0.000045]
            DECIMAL = 7
        
        # ETH Not avaliable.
        class Approve:
            TOKENS = ['USDT', 'USDC', 'WETH', 'WBTC']

            AMOUNT = [0.000025, 0.000045]
            DECIMAL = 7

        class Transfer:
            TOKENS = ['ETH']

            AMOUNT = [0.000025, 0.000045]
            DECIMAL = 7

    class MintNFT:
        NFT_ADDRESS = ''