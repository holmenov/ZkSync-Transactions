import asyncio
import io
import random
import secrets
import sys
import eth_account
from loguru import logger
import pandas as pd
from web3 import Web3
import msoffcrypto

from settings import MainSettings as SETTINGS
from utils.config import API_KEYS


async def async_sleep(sleep_from: int, sleep_to: int, logs: bool = True, account_id: int = 0, key: str = '', msg: str = ''):
    delay = random.randint(sleep_from, sleep_to)
    
    if logs:
        if not msg:
            logger.info(f'Account №{account_id} | {get_wallet_address(key)} | Sleep {delay} seconds.')
        else:
            logger.info(f'Account №{account_id} | {get_wallet_address(key)} | Sleep {delay} seconds, {msg}.')

    for _ in range(delay): await asyncio.sleep(1)

def get_random_address():
    random_bytes = secrets.token_bytes(20)
    evm_address = '0x' + random_bytes.hex()
    random_address = Web3.to_checksum_address(evm_address)
    
    return random_address

def get_wallet_address(key: str) -> str:
    account = eth_account.Account.from_key(key)
    return account.address

def parse_api_keys(password: str | None = None) -> dict:
    decrypted_data = io.BytesIO()
    with open('wallets_data.xlsx', 'rb') as file:
        if SETTINGS.EXCEL_PASSWORD:
            office_file = msoffcrypto.OfficeFile(file)
            
            try:
                office_file.load_key(password=password)
                office_file.decrypt(decrypted_data)
            except msoffcrypto.exceptions.DecryptionError:
                logger.error('Incorrect password to decrypt Excel file or you need set password to file!')
                sys.exit()
        
        try:
            wb = pd.read_excel(decrypted_data if SETTINGS.EXCEL_PASSWORD else file, sheet_name='API')
        except ValueError:
            logger.error('Incorrect page name in Excel file!')
            sys.exit()
        
        API_KEYS['okx_secret_key'] = str(wb.iloc[0]['DATA'])
        API_KEYS['okx_api_key'] = str(wb.iloc[1]['DATA'])
        API_KEYS['okx_passphrase'] = str(wb.iloc[2]['DATA'])
        
        API_KEYS['inch_api_key'] = str(wb.iloc[4]['DATA'])

def parse_wallets():
    decrypted_data = io.BytesIO()
    with open('wallets_data.xlsx', 'rb') as file:
        if SETTINGS.EXCEL_PASSWORD:
            office_file = msoffcrypto.OfficeFile(file)
            
            password = str(input(f'🛡️ Enter the password for the Excel file:'))
            
            try:
                office_file.load_key(password=password)
                office_file.decrypt(decrypted_data)
            except msoffcrypto.exceptions.DecryptionError:
                logger.error('Incorrect password to decrypt Excel file or you need set password to file!')
                sys.exit()
        
        try:
            wb = pd.read_excel(decrypted_data if SETTINGS.EXCEL_PASSWORD else file, sheet_name='WALLETS')
        except ValueError:
            logger.error('Incorrect page name in Excel file!')
            sys.exit()
    
    wallets = []
    for _id, row in wb.iterrows():
        _id += 1
        
        current_wallet = {
            'id': _id,
            'key': str(row['Private Key']) if not pd.isnull(row['Private Key']) else None,
            'proxy': str(row['Proxy']) if not pd.isnull(row['Proxy']) else None
        }
        
        if not current_wallet['key']:
            continue

        if not current_wallet['proxy'] and SETTINGS.USE_PROXY:
            continue
        
        wallets.append(current_wallet)
    
    if not wallets:
        logger.error(f'No wallets were found. Check the entered data!')
    
    parse_api_keys(password if SETTINGS.EXCEL_PASSWORD else None)
    
    return wallets