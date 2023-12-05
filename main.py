from loguru import logger
import questionary

from classes.Threads import Threads
from utils.utils import get_wallets
from utils.modules import *


def get_module():
    modules = [
        questionary.Choice('1) Random Module', random_module),
        questionary.Choice('2) Sending mail via DMail', send_mail),
        questionary.Choice('3) Deposit and withdraw on EraLend', deposit_eraland),
        questionary.Choice('4) Swap on SyncSwap', swap_syncswap),
        questionary.Choice('5) Wrap ETH', wrap_eth),
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