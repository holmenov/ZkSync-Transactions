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
from modules.modules.inch import Inch
from modules.modules.maverick import Maverick
from modules.modules.mute import Mute
from modules.modules.odos import Odos


async def okx_withdraw(account_id: int, key: str, proxy: str):
    okx_withdraw = OKXWithdraw(account_id, key, proxy)
    return await okx_withdraw.withdraw()

async def okx_top_up(account_id: int, key: str, proxy: str):
    amount = OKXSETTINGS.BALANCE_TOP_UP
    
    okx_top_up = OKXTopUp(account_id, key, proxy)
    return await okx_top_up.top_up_balance(amount)

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
    return await syncswap.swap(
        from_token, to_token, min_amount, max_amount, decimal, all_amount, min_percent, max_percent, swap_reverse
    )

async def swap_inch(account_id, key, proxy):
    from_token = ms.Inch.FROM_TOKEN
    to_token = ms.Inch.TO_TOKEN
    
    min_amount = ms.Inch.AMOUNT[0]
    max_amount = ms.Inch.AMOUNT[1]
    decimal = ms.Inch.DECIMAL
    
    all_amount = ms.Inch.USE_PERCENTS
    
    swap_reverse = ms.Inch.SWAP_REVERSE
    
    min_percent = ms.Inch.PERCENTS[0]
    max_percent = ms.Inch.PERCENTS[1]
    
    inch = Inch(account_id, key, proxy)
    return await inch.swap(
        from_token, to_token, min_amount, max_amount, decimal, all_amount, min_percent, max_percent, swap_reverse
    )

async def swap_maverick(account_id, key, proxy):
    from_token = ms.Maverick.FROM_TOKEN
    to_token = ms.Maverick.TO_TOKEN
    
    min_amount = ms.Maverick.AMOUNT[0]
    max_amount = ms.Maverick.AMOUNT[1]
    decimal = ms.Maverick.DECIMAL
    
    all_amount = ms.Maverick.USE_PERCENTS
    
    swap_reverse = ms.Maverick.SWAP_REVERSE
    
    min_percent = ms.Maverick.PERCENTS[0]
    max_percent = ms.Maverick.PERCENTS[1]
    
    maverick = Maverick(account_id, key, proxy)
    return await maverick.swap(
        from_token, to_token, min_amount, max_amount, decimal, all_amount, min_percent, max_percent, swap_reverse
    )

async def swap_mute(account_id, key, proxy):
    from_token = ms.Mute.FROM_TOKEN
    to_token = ms.Mute.TO_TOKEN
    
    min_amount = ms.Mute.AMOUNT[0]
    max_amount = ms.Mute.AMOUNT[1]
    decimal = ms.Mute.DECIMAL
    
    all_amount = ms.Mute.USE_PERCENTS
    
    swap_reverse = ms.Mute.SWAP_REVERSE
    
    min_percent = ms.Mute.PERCENTS[0]
    max_percent = ms.Mute.PERCENTS[1]
    
    mute = Mute(account_id, key, proxy)
    return await mute.swap(
        from_token, to_token, min_amount, max_amount, decimal, all_amount, min_percent, max_percent, swap_reverse
    )
    
async def swap_odos(account_id, key, proxy):
    from_token = ms.Odos.FROM_TOKEN
    to_token = ms.Odos.TO_TOKEN
    
    min_amount = ms.Odos.AMOUNT[0]
    max_amount = ms.Odos.AMOUNT[1]
    decimal = ms.Odos.DECIMAL
    
    all_amount = ms.Odos.USE_PERCENTS
    
    swap_reverse = ms.Odos.SWAP_REVERSE
    
    min_percent = ms.Odos.PERCENTS[0]
    max_percent = ms.Odos.PERCENTS[1]
    
    odos = Odos(account_id, key, proxy)
    return await odos.swap(
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
    return await eralend.deposit(
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
    return await wrap_eth.wrap_eth(
        min_amount, max_amount, decimal, all_amount, min_percent, max_percent, unwrap_eth
    )

async def send_mail(account_id, key, proxy):
    dmail = Dmail(account_id, key, proxy)
    return await dmail.send_mail()

async def mint_nft(account_id, key, proxy):
    nft_address = ms.MintNFT.NFT_ADDRESS
    
    mint_nft = MintNFT(account_id, key, proxy)
    return await mint_nft.mint_nft(nft_address)

async def rubyscore_vote(account_id, key, proxy):
    rubyscore = RubyScore(account_id, key, proxy)
    return await rubyscore.vote()

async def owlto_checkin(account_id, key, proxy):
    owlto = OwlTo(account_id, key, proxy)
    return await owlto.check_in()

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