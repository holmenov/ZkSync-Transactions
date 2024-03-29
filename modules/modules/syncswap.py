import time
from loguru import logger
from eth_abi import abi

from modules.account import Account
from settings import MainSettings as SETTINGS
from utils.config import SYNCSWAP_CLASSIC_POOL_ABI, SYNCSWAP_CLASSIC_POOL_DATA_ABI, SYNCSWAP_CONTRACTS, SYNCSWAP_ROUTER_ABI, ZERO_ADDRESS, ZKSYNC_TOKENS
from utils.utils import async_sleep
from utils.wrappers import check_gas

class SyncSwap(Account):
    def __init__(self, account_id: int, private_key: str, proxy: str | None) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        
        self.swap_contract = self.get_contract(SYNCSWAP_CONTRACTS["router"], SYNCSWAP_ROUTER_ABI)
    
    async def get_pool(self, from_token: str, to_token: str):
        contract = self.get_contract(SYNCSWAP_CONTRACTS['classic_pool'], SYNCSWAP_CLASSIC_POOL_ABI)
        
        pool_address = await contract.functions.getPool(
            self.w3.to_checksum_address(ZKSYNC_TOKENS[from_token]),
            self.w3.to_checksum_address(ZKSYNC_TOKENS[to_token])
        ).call()

        return pool_address
    
    async def get_min_amount_out(self, pool_address: str, token_address: str, amount: int):
        pool_contract = self.get_contract(pool_address, SYNCSWAP_CLASSIC_POOL_DATA_ABI)
        
        min_amount_out = await pool_contract.functions.getAmountOut(
            token_address,
            amount,
            self.address
        ).call()
        
        return int(min_amount_out - (min_amount_out / 100 * SETTINGS.SLIPPAGE))
    
    @check_gas
    async def swap(
        self,
        from_token: str,
        to_token: str,
        min_amount: float,
        max_amount: float,
        decimal: int,
        all_amount: bool,
        min_percent: int,
        max_percent: int,
        swap_reverse: bool
    ):
        try:
            self.log_send(f'{from_token} -> {to_token} | Swap on SyncSwap.')

            if all_amount:
                amount_wei, _ = await self.get_percent_amount(from_token, min_percent, max_percent)
            else:
                amount_wei, _ = await self.get_random_amount(from_token, min_amount, max_amount, decimal)

            token_address = self.w3.to_checksum_address(ZKSYNC_TOKENS[from_token])

            pool_address = await self.get_pool(from_token, to_token)
            
            if pool_address == ZERO_ADDRESS:
                return self.log_send(f'Swap path {from_token} to {to_token} not found!', status='error')
            
            if from_token != 'ETH':
                await self.approve(amount_wei, token_address, self.w3.to_checksum_address(SYNCSWAP_CONTRACTS['router']))
            
            tx_data = await self.get_tx_data(value=amount_wei if from_token == 'ETH' else 0)
            
            min_amount_out = await self.get_min_amount_out(pool_address, token_address, amount_wei)
            
            steps = [{
                'pool': pool_address,
                'data': abi.encode(['address', 'address', 'uint8'], [token_address, self.address, 1]),
                'callback': ZERO_ADDRESS,
                'callbackData': '0x'
            }]
            
            paths = [{
                'steps': steps,
                'tokenIn': ZERO_ADDRESS if from_token == 'ETH' else token_address,
                'amountIn': amount_wei
            }]
            
            deadline = int(time.time()) + 10000000
            
            tx = await self.swap_contract.functions.swap(
                paths,
                min_amount_out,
                deadline
            ).build_transaction(tx_data)
            
            tx_status = await self.execute_transaction(tx)

            if swap_reverse:
                await async_sleep(5, 15, logs=False)
                await self.swap(to_token, from_token, 0.01, 0.01, decimal, True, 100, 100, False)
            else:
                return tx_status
        
        except Exception as e:
            self.log_send(f'Error in module «{__class__.__name__}»: {e}', status='error')
            return False