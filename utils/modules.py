import random
from modules.mint_nft import MintNFT

import modules_settings as ms
from modules.dmail import Dmail
from modules.eralend import Eralend
from modules.syncswap import SyncSwap
from modules.wrap_eth import WrapETH


async def random_module(account_id, key, proxy):
    modules = [send_mail, deposit_eraland, swap_syncswap, wrap_eth, mint_nft]
    choice = random.choice(modules)
    await choice(account_id, key, proxy)

async def random_low_cost_module(account_id, key, proxy):
    modules = [send_mail, wrap_eth, deposit_eraland]
    choice = random.choice(modules)
    await choice(account_id, key, proxy)


async def send_mail(account_id, key, proxy):
    dmail = Dmail(account_id, key, proxy)
    await dmail.send_mail()
    
async def deposit_eraland(account_id, key, proxy):
    min_amount = ms.EraLend.min_amount
    max_amount = ms.EraLend.max_amount
    decimal = ms.EraLend.decimal
    
    all_amount = ms.EraLend.all_amount
    min_percent = ms.EraLend.min_percent
    max_percent = ms.EraLend.max_percent

    make_withdraw = ms.EraLend.make_withdraw
    
    eralend = Eralend(account_id, key, proxy)
    await eralend.deposit(
        min_amount, max_amount, decimal, all_amount, min_percent, max_percent, make_withdraw
    )

async def swap_syncswap(account_id, key, proxy):
    from_token = ms.SyncSwap.from_token
    to_token = ms.SyncSwap.to_token
    
    min_amount = ms.SyncSwap.min_amount
    max_amount = ms.SyncSwap.max_amount
    decimal = ms.SyncSwap.decimal
    
    all_amount = ms.SyncSwap.all_amount
    
    swap_reverse = ms.SyncSwap.swap_reverse
    
    min_percent = ms.SyncSwap.min_percent
    max_percent = ms.SyncSwap.max_percent
    
    syncswap = SyncSwap(account_id, key, proxy)
    await syncswap.swap(
        from_token, to_token, min_amount, max_amount, decimal, all_amount, min_percent, max_percent, swap_reverse
    )
    
async def wrap_eth(account_id, key, proxy):
    min_amount = ms.WrapETH.min_amount
    max_amount = ms.WrapETH.max_amount
    decimal = ms.WrapETH.decimal
    
    all_amount = ms.WrapETH.all_amount
    min_percent = ms.WrapETH.min_percent
    max_percent = ms.WrapETH.max_percent
    
    unwrap_eth = ms.WrapETH.unwrap_eth
    
    wrap_eth = WrapETH(account_id, key, proxy)
    await wrap_eth.wrap_eth(
        min_amount, max_amount, decimal, all_amount, min_percent, max_percent, unwrap_eth
    )

async def mint_nft(account_id, key, proxy):
    nft_address = ms.MintNFT.nft_address
    
    mint_nft = MintNFT(account_id, key, proxy)
    await mint_nft.mint_nft(nft_address)