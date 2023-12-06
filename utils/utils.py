import asyncio
import random
import sys
from typing import Callable
import eth_account

from loguru import logger
from utils.config import ACCOUNTS, PROXIES
from settings import REMOVE_WALLET, SLEEP_AFTER_WORK_FROM, SLEEP_AFTER_WORK_TO, USE_PROXY


async def sleep(sleep_from: int, sleep_to: int):
    delay = random.randint(sleep_from, sleep_to)
    
    logger.info(f'💤 Sleep {delay} s.')
    for _ in range(delay):
        await asyncio.sleep(1)

def _async_run_module(module: Callable, account_id: int, key: str, proxy: str):
    try:
        asyncio.run(run_module(module, account_id, key, proxy))
    except Exception as e:
        logger.error(f'ID: {account_id} | {get_wallet_address(key)} | An error occurred: {e}.')

    if REMOVE_WALLET:
        remove_wallet_from_files(key, proxy)

async def run_module(module, account_id, key, proxy):
    await module(account_id, key, proxy)
    await sleep(SLEEP_AFTER_WORK_FROM, SLEEP_AFTER_WORK_TO)
    
def get_wallet_address(key: str) -> str:
    account = eth_account.Account.from_key(key)
    return account.address

def get_wallets():
    if len(ACCOUNTS) != len(PROXIES):
        logger.error('The number of wallets and proxies does not match.')
        sys.exit()
    
    elif len(ACCOUNTS) < 1:
        logger.error('It seems you forgot to enter the wallets.')
        sys.exit()
    
    accounts_proxy = dict(zip(ACCOUNTS, PROXIES)) if USE_PROXY else ACCOUNTS

    wallets = [
        {
            'id': _id,
            'key': key,
            'proxy': accounts_proxy[key] if USE_PROXY else None
        } for _id, key in enumerate(accounts_proxy, start=1)
    ]

    return wallets

def remove_wallet_from_files(account_to_remove: str, proxy_to_remove: str):
    with open('accounts.txt', 'r', encoding='utf-8') as accounts_file:
        accounts = accounts_file.readlines()
    with open('proxy.txt', 'r', encoding='utf-8') as proxy_file:
        proxies = proxy_file.readlines()
    
    cleared_accounts = [account for account in accounts if account.strip() != account_to_remove]
    cleared_proxies = [proxy for proxy in proxies if proxy.strip() != proxy_to_remove]
    
    with open('accounts.txt', 'w', encoding='utf-8') as accounts_file:
        accounts_file.writelines(cleared_accounts)
    with open('proxy.txt', 'w', encoding='utf-8') as proxy_file:
        proxy_file.writelines(cleared_proxies)