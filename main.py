from loguru import logger
import questionary

from classes.Threads import Threads
from utils.utils import get_wallets
from utils.modules import *


def get_module():
    modules = [
        questionary.Choice('1) Random module', random_module),
        questionary.Choice('2) Random low-cost module', random_low_cost_module),
        questionary.Choice('3) Sending mail via DMail', send_mail),
        questionary.Choice('4) Deposit and withdraw on EraLend', deposit_eraland),
        questionary.Choice('5) Swap on SyncSwap', swap_syncswap),
        questionary.Choice('6) Wrap ETH', wrap_eth),
        questionary.Choice('7) Mint NFT', mint_nft),
    ]
    
    module = questionary.select(
        'Choose module to start:',
        choices=modules,
        qmark='📌 ',
        pointer='➡️ '
    ).ask()

    return module

def main():
    module = get_module()
    data = get_wallets()

    threads = Threads(data)
    threads.start_workers(module=module)

if __name__ == '__main__':
    logger.add('logs.log')
    main()