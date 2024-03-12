import random

from settings import ModulesSettings as ms
from settings import OKXSettings as OKXSETTINGS
from modules.modules.dmail import Dmail
from modules.modules.eralend import Eralend
from modules.modules.syncswap import SyncSwap
from modules.modules.wrap_eth import WrapETH
from modules.modules.mint_nft import MintNFT
from modules.modules.okx_withdraw import OKXWithdraw
from modules.modules.rubyscore import RubyScore
from modules.modules.owlto import OwlTo
from modules.modules.okx_topup import OKXTopUp
from modules.modules.tokens import Tokens
from modules.modules.balance_checker import BalanceChecker
from modules.modules.woofi import WooFi


async def random_module(account_id, key, proxy):
    modules = [send_mail, deposit_eraland, swap_syncswap, wrap_eth, mint_nft]
    choice = random.choice(modules)
    await choice(account_id, key, proxy)

async def random_low_cost_module(account_id, key, proxy):
    modules = [send_mail, wrap_eth, deposit_eraland, owlto_checkin, rubyscore_vote]
    choice = random.choice(modules)
    await choice(account_id, key, proxy)


async def okx_withdraw(account_id: int, key: str, proxy: str):
    okx_withdraw = OKXWithdraw(account_id, key, proxy)
    await okx_withdraw.withdraw()


async def okx_top_up(account_id: int, key: str, proxy: str):
    amount = OKXSETTINGS.BALANCE_TOP_UP
    
    okx_top_up = OKXTopUp(account_id, key, proxy)
    await okx_top_up.top_up_balance(amount)


async def swap_syncswap(account_id, key, proxy):
    from_token = ms.SyncSwap.FROM_TOKEN
    to_token = ms.SyncSwap.TO_TOKEN
    
    min_amount = ms.SyncSwap.AMOUNT[0]
    max_amount = ms.SyncSwap.AMOUNT[1]
    decimal = ms.SyncSwap.DECIMAL
    
    all_amount = ms.SyncSwap.USE_PERCENTS
    
    swap_reverse = ms.SyncSwap.SWAP_REVERSE
    
    min_percent = ms.SyncSwap.PERCENTS[0]
    max_percent = ms.SyncSwap.PERCENTS[1]
    
    syncswap = SyncSwap(account_id, key, proxy)
    await syncswap.swap(
        from_token, to_token, min_amount, max_amount, decimal, all_amount, min_percent, max_percent, swap_reverse
    )

async def swap_woofi(account_id, key, proxy):
    from_token = ms.WooFi.FROM_TOKEN
    to_token = ms.WooFi.TO_TOKEN
    
    min_amount = ms.WooFi.AMOUNT[0]
    max_amount = ms.WooFi.AMOUNT[1]
    decimal = ms.WooFi.DECIMAL
    
    all_amount = ms.WooFi.USE_PERCENTS
    
    swap_reverse = ms.WooFi.SWAP_REVERSE
    
    min_percent = ms.WooFi.PERCENTS[0]
    max_percent = ms.WooFi.PERCENTS[1]
    
    woofi = WooFi(account_id, key, proxy)
    await woofi.swap(
        from_token, to_token, min_amount, max_amount, decimal, all_amount, min_percent, max_percent, swap_reverse
    )
    
async def deposit_eraland(account_id, key, proxy):
    min_amount = ms.EraLend.AMOUNT[0]
    max_amount = ms.EraLend.AMOUNT[1]
    decimal = ms.EraLend.DECIMAL
    
    all_amount = ms.EraLend.USE_PERCENTS
    min_percent = ms.EraLend.PERCENTS[0]
    max_percent = ms.EraLend.PERCENTS[1]

    make_withdraw = ms.EraLend.WITHDRAW
    
    eralend = Eralend(account_id, key, proxy)
    await eralend.deposit(
        min_amount, max_amount, decimal, all_amount, min_percent, max_percent, make_withdraw
    )
    
async def wrap_eth(account_id, key, proxy):
    min_amount = ms.WrapETH.AMOUNT[0]
    max_amount = ms.WrapETH.AMOUNT[1]
    decimal = ms.WrapETH.DECIMAL
    
    all_amount = ms.WrapETH.USE_PERCENTS
    min_percent = ms.WrapETH.PERCENTS[0]
    max_percent = ms.WrapETH.PERCENTS[1]
    
    unwrap_eth = ms.WrapETH.UNWRAP_ETH
    
    wrap_eth = WrapETH(account_id, key, proxy)
    await wrap_eth.wrap_eth(
        min_amount, max_amount, decimal, all_amount, min_percent, max_percent, unwrap_eth
    )

async def send_mail(account_id, key, proxy):
    dmail = Dmail(account_id, key, proxy)
    await dmail.send_mail()

async def mint_nft(account_id, key, proxy):
    nft_address = ms.MintNFT.NFT_ADDRESS
    
    mint_nft = MintNFT(account_id, key, proxy)
    await mint_nft.mint_nft(nft_address)

async def rubyscore_vote(account_id, key, proxy):
    rubyscore = RubyScore(account_id, key, proxy)
    await rubyscore.vote()

async def owlto_checkin(account_id, key, proxy):
    owlto = OwlTo(account_id, key, proxy)
    await owlto.check_in()

async def increase_allowance(account_id, key, proxy):
    tokens = ms.Tokens.IncreaseAllowance.TOKENS
    
    min_amount = ms.Tokens.IncreaseAllowance.AMOUNT[0]
    max_amount = ms.Tokens.IncreaseAllowance.AMOUNT[1]
    decimals = ms.Tokens.IncreaseAllowance.DECIMAL
    
    tokens_functions = Tokens(account_id, key, proxy)
    return await tokens_functions.increase_allowance(
        tokens, min_amount, max_amount, decimals
    )

async def approve(account_id, key, proxy):
    tokens = ms.Tokens.Approve.TOKENS
    
    min_amount = ms.Tokens.Approve.AMOUNT[0]
    max_amount = ms.Tokens.Approve.AMOUNT[1]
    decimals = ms.Tokens.Approve.DECIMAL
    
    tokens_functions = Tokens(account_id, key, proxy)
    return await tokens_functions.approve_random_address(
        tokens, min_amount, max_amount, decimals
    )

async def transfer(account_id, key, proxy):
    tokens = ms.Tokens.Transfer.TOKENS
    
    min_amount = ms.Tokens.Transfer.AMOUNT[0]
    max_amount = ms.Tokens.Transfer.AMOUNT[1]
    decimals = ms.Tokens.Transfer.DECIMAL
    
    tokens_functions = Tokens(account_id, key, proxy)
    return await tokens_functions.transfer(
        tokens, min_amount, max_amount, decimals
    )

async def check_balance(account_id, key, proxy):
    balance_checker = BalanceChecker(account_id, key, proxy)
    return await balance_checker.check_balance()