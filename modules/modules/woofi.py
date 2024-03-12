from modules.account import Account
from utils.config import WOOFI_ABI, WOOFI_CONTRACTS, ZKSYNC_TOKENS
from settings import MainSettings as SETTINGS
from utils.utils import async_sleep
from utils.wrappers import check_gas


class WooFi(Account):
    def __init__(self, account_id: int, private_key: str, proxy: str | None, chain: str = 'zksync') -> None:
        super().__init__(account_id, private_key, proxy, chain)
    
        self.woofi_contract = self.get_contract(WOOFI_CONTRACTS["router"], WOOFI_ABI)
    
    async def get_min_amount_out(self, from_token: str, to_token: str, amount: int):
        min_amount_out = await self.woofi_contract.functions.querySwap(
            self.w3.to_checksum_address(from_token),
            self.w3.to_checksum_address(to_token),
            amount
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
        self.log_send(f'{from_token} -> {to_token} | Swap on WooFi.')

        if all_amount:
            amount_wei, _ = await self.get_percent_amount(from_token, min_percent, max_percent)
        else:
            amount_wei, _ = await self.get_random_amount(from_token, min_amount, max_amount, decimal)

        token_address = self.w3.to_checksum_address(ZKSYNC_TOKENS[from_token])

        tx_data = await self.get_tx_data()
        
        if from_token == 'ETH':
            tx_data.update({'value': amount_wei})
        else:
            await self.approve(amount_wei, token_address, self.w3.to_checksum_address(WOOFI_CONTRACTS['router']))
            
        min_amount_out = await self.get_min_amount_out(ZKSYNC_TOKENS[from_token], ZKSYNC_TOKENS[to_token], amount_wei)
        
        tx = await self.woofi_contract.functions.swap(
            self.w3.to_checksum_address(ZKSYNC_TOKENS[from_token]),
            self.w3.to_checksum_address(ZKSYNC_TOKENS[to_token]),
            amount_wei,
            min_amount_out,
            self.address,
            self.address
        ).build_transaction(tx_data)
        
        await self.execute_transaction(tx)
        
        if swap_reverse:
            await async_sleep(5, 15, logs=False)

            await self.swap(to_token, from_token, 0.01, 0.01, decimal, True, 100, 100, False)