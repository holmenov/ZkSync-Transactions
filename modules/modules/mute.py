import time

from modules.account import Account
from utils.config import MUTE_CONTRACTS, MUTE_ROUTER_ABI, ZKSYNC_TOKENS
from settings import MainSettings as SETTINGS
from utils.utils import async_sleep
from utils.wrappers import check_gas


class Mute(Account):
    def __init__(self, account_id: int, private_key: str, proxy: str | None) -> None:
        super().__init__(account_id, private_key, proxy)
    
        self.swap_contract = self.get_contract(MUTE_CONTRACTS["router"], MUTE_ROUTER_ABI)
    
    async def get_min_amount_out(self, from_token: str, to_token: str, amount_wei: int):
        min_amount_out = await self.swap_contract.functions.getAmountOut(
            amount_wei,
            self.w3.to_checksum_address(from_token),
            self.w3.to_checksum_address(to_token)
        ).call()

        return int(min_amount_out[0] - (min_amount_out[0] / 100 * SETTINGS.SLIPPAGE))

    async def swap_to_token(self, from_token: str, to_token: str, amount_wei: int):
        tx_data = await self.get_tx_data(value=amount_wei)

        deadline = int(time.time()) + 1000000

        min_amount_out = await self.get_min_amount_out(ZKSYNC_TOKENS[from_token], ZKSYNC_TOKENS[to_token], amount_wei)

        contract_txn = await self.swap_contract.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(
            min_amount_out,
            [
                self.w3.to_checksum_address(ZKSYNC_TOKENS[from_token]),
                self.w3.to_checksum_address(ZKSYNC_TOKENS[to_token])
            ],
            self.address,
            deadline,
            [False, False]
        ).build_transaction(tx_data)

        return contract_txn

    async def swap_to_eth(self, from_token: str, to_token: str, amount_wei: int):
        token_address = self.w3.to_checksum_address(ZKSYNC_TOKENS[from_token])

        from_token_stable = True if from_token == "USDC" else False

        await self.approve(amount_wei, token_address, MUTE_CONTRACTS["router"])

        tx_data = await self.get_tx_data()
        
        deadline = int(time.time()) + 1000000

        min_amount_out = await self.get_min_amount_out(ZKSYNC_TOKENS[from_token], ZKSYNC_TOKENS[to_token], amount_wei)

        contract_txn = await self.swap_contract.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
            amount_wei,
            min_amount_out,
            [
                self.w3.to_checksum_address(ZKSYNC_TOKENS[from_token]),
                self.w3.to_checksum_address(ZKSYNC_TOKENS[to_token])
            ],
            self.address,
            deadline,
            [from_token_stable, False]
        ).build_transaction(tx_data)

        return contract_txn
    
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
            self.log_send(f'{from_token} -> {to_token} | Swap on Mute.')
            
            if all_amount:
                amount_wei, _ = await self.get_percent_amount(from_token, min_percent, max_percent)
            else:
                amount_wei, _ = await self.get_random_amount(from_token, min_amount, max_amount, decimal)

            if from_token == "ETH":
                tx = await self.swap_to_token(from_token, to_token, amount_wei)
            else:
                tx = await self.swap_to_eth(from_token, to_token, amount_wei)

            tx_status = await self.execute_transaction(tx)

            if swap_reverse:
                await async_sleep(5, 15, logs=False)
                await self.swap(to_token, from_token, 0.01, 0.01, decimal, True, 100, 100, False)
            else:
                return tx_status
        
        except Exception as e:
            self.log_send(f'Error in module «{__class__.__name__}»: {e}', status='error')
            return False