import asyncio
from loguru import logger
import questionary
import sys

from utils.launch import run_check_balance, start_tasks
from utils.utils import get_wallets
from utils.modules import *


def start():
    start_menu = [
        questionary.Choice('🚀 Custom Module Routes', 'custom-routes'),
        questionary.Choice('✨ One Selected Module', 'one-module'),
        questionary.Choice('💼 zkSync Balance Checker', 'balance-checker'),
        questionary.Choice('❌ Exit', 'exit'),
    ]
    
    start_mode = questionary.select(
        'Select a mode to start the software:',
        choices=start_menu,
        qmark='📌 ',
        pointer='➡️ '
    ).ask()
    
    return start_mode


def one_selected_module():
    modules = [
        questionary.Choice('● Swap on SyncSwap', swap_syncswap),
        questionary.Choice('● Swap on WooFi', swap_woofi),
        questionary.Choice('● Deposit on EraLend', deposit_eraland),
        questionary.Choice('● Wrap ETH', wrap_eth),
        questionary.Choice('● Sending mail via DMail', send_mail),
        questionary.Choice('● Mint NFT', mint_nft),
        questionary.Choice('● Vote on RubyScore', rubyscore_vote),
        questionary.Choice('● Daily check in on OwlTo', owlto_checkin),
        questionary.Choice('● Increase allowance token', increase_allowance),
        questionary.Choice('● Approve token', approve),
        questionary.Choice('● Transfer token', transfer),
        questionary.Choice('● OKX Withdraw', okx_withdraw),
        questionary.Choice('● OKX Top Up', okx_top_up),
        questionary.Choice('● Random cheap module', random_low_cost_module),
        questionary.Choice('● Random module', random_module),
    ]
    
    module = questionary.select(
        'Choose module to start:',
        choices=modules,
        qmark='📌 ',
        pointer='➡️ '
    ).ask()

    return module


def main():
    start_mode = start()
    
    if start_mode == 'exit': sys.exit()
    
    data = get_wallets()
    
    if start_mode == 'custom-routes':
        asyncio.run(start_tasks(data))

    elif start_mode == 'one-module':
        module = one_selected_module()
        asyncio.run(start_tasks(data, module))

    elif start_mode == 'balance-checker':
        asyncio.run(run_check_balance(data))
    

if __name__ == '__main__':
    logger.add('logs.log')
    main()