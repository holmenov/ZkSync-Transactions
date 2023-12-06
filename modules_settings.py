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