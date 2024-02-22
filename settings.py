# ==========================================================
#                       MAIN SETTINGS
# ==========================================================


class MainSettings:
    # Gwei control
    MAX_GAS = 45

    # Gas multiplayer
    GAS_MULTIPLAYER = 0.8

    # Take the wallets in random order
    RANDOM_WALLETS = True

    # Remove wallet from files after work
    REMOVE_WALLET = True

    # Proxy mode
    USE_PROXY = True

    # Period in seconds to run all wallets
    START_PERIOD_FROM = 1
    START_PERIOD_TO = 1800
    
    # Module repetitions for each wallet
    REPEATS_PER_WALLET = 1

    # Sleeps after work
    SLEEP_AFTER_WORK_FROM = 60 # Seconds
    SLEEP_AFTER_WORK_TO = 150 # Seconds

    # RPC
    ZKSYNC_RPC = 'https://mainnet.era.zksync.io'

    # SLIPPAGE FOR SWAPS
    SLIPPAGE = 5


# ===========================================================
#                       OKX SETTINGS
# ===========================================================


class OKXSettings:
    # You can find this data when withdrawing funds to OKX
    SYMBOL = 'ETH'
    CHAIN = 'zkSync Era'
    FEE = 0.00015
    
    # Withdrawal amount (For Withdraw Module)
    AMOUNT_FROM = 0.006
    AMOUNT_TO = 0.008
    
    # OKX Top Up (For Top Up Module)
    MIN_AMOUNT = 0.0125
    MAX_AMOUNT = 0.0105
    DECIMALS = 5

    # Here you can get your api-key: https://www.okx.cab/ru/account/my-api
    SECRET_KEY = 'YOUR_DATA'
    API_KEY = 'YOUR_DATA'
    PASSPHRASE = 'YOUR_DATA'


# ===========================================================
#                       ROUTES SETTINGS
# ===========================================================


class ModulesSettings:
    
    class EraLend:
        min_amount = 0.0005
        max_amount = 0.0009
        decimal = 5
        
        all_amount = False
        min_percent = 5
        max_percent = 5
        
        make_withdraw = True

    class SyncSwap:
        from_token = 'ETH'
        to_token = 'USDC'
        
        min_amount = 0.0005
        max_amount = 0.0009
        decimal = 5
        
        all_amount = False
        
        swap_reverse = True
        
        min_percent = 100
        max_percent = 100

    class WrapETH:
        min_amount = 0.0005
        max_amount = 0.0009
        decimal = 5
        
        all_amount = False
        min_percent = 10
        max_percent = 15
        
        unwrap_eth = True

    class MintNFT:
        nft_address = ''