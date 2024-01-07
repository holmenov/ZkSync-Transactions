import asyncio
import random

import eth_account
from loguru import logger
from web3 import AsyncWeb3
from web3.middleware import async_geth_poa_middleware
from web3.types import TxParams
from web3.exceptions import TransactionNotFound
from settings import MainSettings as SETTINGS

from utils.config import ERC20_ABI, MAX_APPROVE, ZKSYNC_TOKENS
from utils.utils import async_sleep


class Account:
    def __init__(self, account_id: int, private_key: str, proxy: str | None) -> None:
        self.account_id = account_id
        self.private_key = private_key
        self.explorer = 'https://explorer.zksync.io/tx/'

        request_kwargs = {}
        
        if proxy:
            request_kwargs = {'proxy': f'http://{proxy}'}
            
        self.w3 = AsyncWeb3(
            AsyncWeb3.AsyncHTTPProvider(SETTINGS.ZKSYNC_RPC),
            middlewares=[async_geth_poa_middleware],
            request_kwargs=request_kwargs
        )

        self.address = eth_account.Account.from_key(private_key).address
    
    @staticmethod
    def wei_to_eth(amount_wei: int, decimals: int = 18) -> float:
        return amount_wei / (10 ** decimals)
    
    @staticmethod
    def eth_to_wei(amount_eth: float, decimals: int = 18) -> int:
        return amount_eth * (10 ** decimals)
    
    async def get_allowance(self, token_address: str, contract_address: str):
        token_address = self.w3.to_checksum_address(token_address)
        contract_address = self.w3.to_checksum_address(contract_address)
        
        contract = self.w3.eth.contract(address=token_address, abi=ERC20_ABI)
        amount_approved = await contract.functions.allowance(self.address, contract_address).call()
        
        return amount_approved
    
    async def approve(self, amount: int, token_address: str, contract_address: str):
        token_address = self.w3.to_checksum_address(token_address)
        contract_address = self.w3.to_checksum_address(contract_address)
        
        contract = self.w3.eth.contract(address=token_address, abi=ERC20_ABI)
        allowance_amount = await self.check_allowance(token_address, contract_address)
        
        if amount > allowance_amount:
            logger.success(f'{self.account_id} | {self.address} | Make approve')

            tx_data = await self.get_tx_data()
            tx = await contract.functions.approve(contract_address, MAX_APPROVE).build_transaction(tx_data)
            await self.execute_transaction(tx)

            await async_sleep(5, 10, logs=False)
    
    async def execute_transaction(self, tx: TxParams, wait_complete: bool = True):
        signed_tx = await self.sign(tx)
        tx_hash = await self.send_raw_transaction(signed_tx)
        
        if wait_complete:
            await self.wait_until_tx_finished(tx_hash)
        else:
            return tx_hash
    
    async def get_balance(self, contract_address: str) -> dict:
        contract_address = self.w3.to_checksum_address(contract_address)
        contract = self.get_contract(contract_address)

        symbol = await contract.functions.symbol().call()
        decimal = await contract.functions.decimals().call()
        balance_wei = await contract.functions.balanceOf(self.address).call()

        balance = Account.wei_to_eth(balance_wei, decimal)

        return {"balance_wei": balance_wei, "balance": balance, "symbol": symbol, "decimal": decimal}
    
    async def get_amount(
        self,
        token: str,
        min_amt: float = 0,
        max_amt: float = 0,
        use_percents: bool = False,
        min_pct: int = 0,
        max_pct: int = 0,
        decimal: int = 6
    ):
        if not use_percents:
            if min_amt == max_amt == 0:
                raise ValueError("Not declared values for 'min_amt' and 'max_amt'.")
            rnd_pct = random.randint(min_pct, max_pct) / 100
        else:
            if min_pct == max_pct == 0:
                raise ValueError("Not declared values for 'min_pct' and 'max_pct'.")
            rnd_amt = round(random.uniform(min_amt, max_amt), decimal)

        if token == 'ETH':
            balance_wei = await self.w3.eth.get_balance(self.address)
            amt_wei = int(balance_wei * rnd_pct) if use_percents else self.w3.to_wei(rnd_amt, 'ether')
            amt = self.w3.from_wei(int(balance_wei * rnd_pct), 'ether') if use_percents else rnd_amt
        else:
            balance = await self.get_balance(ZKSYNC_TOKENS[token])
            amt_wei = int(balance['balance_wei'] * rnd_pct) if use_percents else Account.eth_to_wei(rnd_amt, balance['decimal'])
            amt = balance['balance'] * rnd_pct if use_percents else rnd_amt
            balance = balance['balance_wei']
        
        return amt_wei, amt, balance
    
    def get_contract(self, contract_address: str, abi = None):
        contract_address = self.w3.to_checksum_address(contract_address)
        abi = ERC20_ABI if abi is None else abi
        contract = self.w3.eth.contract(address=contract_address, abi=abi)

        return contract
    
    async def get_tx_data(self, value: int = 0, eip_1559: bool = True):
        tx = {
            'chainId': await self.w3.eth.chain_id,
            'from': self.address,
            'value': value,
            'nonce': await self.w3.eth.get_transaction_count(self.address)
        }
        
        if eip_1559:
            base_fee = (await self.w3.eth.get_block('latest'))['baseFeePerGas']
            tx.update({
                'maxFeePerGas': base_fee,
                'maxPriorityFeePerGas': base_fee,
                'type': '0x2'
            })

        else:
            tx['gasPrice'] = await self.w3.eth.gas_price
        
        return tx
    
    async def sign(self, transaction):
        gas = await self.w3.eth.estimate_gas(transaction)
        gas = int(gas * SETTINGS.GAS_MULTIPLAYER)
        
        transaction.update({'gas': gas})
        
        signed_tx = self.w3.eth.account.sign_transaction(transaction, self.private_key)
        return signed_tx
    
    async def send_raw_transaction(self, signed_txn):
        txn_hash = await self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return txn_hash
    
    async def wait_until_tx_finished(self, hash: str):
        attempts_count = 0

        while True:
            try:
                receipts = await self.w3.eth.get_transaction_receipt(hash)
                status = receipts.get('status')

                if status == 1:
                    return logger.success(f'{self.account_id} | {self.address} | {self.explorer}{hash.hex()} successfully!')
                elif status is None:
                    await async_sleep(10, 10, logs=False)
                else:
                    return logger.error(f'{self.account_id} | {self.address} | {self.explorer}{hash.hex()} transaction failed!')
            
            except TransactionNotFound:
                if attempts_count >= 30:
                    return logger.warning(f'{self.account_id} | {self.address} | {self.explorer}{hash.hex()} transaction not found!')
                
                attempts_count += 1
                await asyncio.sleep(10, 10)