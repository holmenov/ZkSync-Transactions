from loguru import logger

from modules.account import Account
from utils.config import WETH_ABI, ZKSYNC_TOKENS
from utils.utils import async_sleep
from utils.wrappers import check_gas


class WrapETH(Account):
    def __init__(self, account_id: int, private_key: str, proxy: str | None) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        
        self.weth_contract = self.get_contract(ZKSYNC_TOKENS['WETH'], WETH_ABI)
    
    @check_gas
    async def wrap_eth(
        self,
        min_amount: float,
        max_amount: float,
        decimal: int,
        all_amount: bool,
        min_percent: int,
        max_percent: int,
        unwrap_eth: bool
    ):
        logger.info(f"{self.account_id} | {self.address} | Wrap ETH.")

        amount_wei, amount, balance = await self.get_amount(
            "ETH",
            min_amount,
            max_amount,
            decimal,
            all_amount,
            min_percent,
            max_percent
        )
        
        tx_data = await self.get_tx_data(value=amount_wei)
        
        tx = await self.weth_contract.functions.deposit().build_transaction(tx_data)
        
        await self.execute_transaction(tx)
        
        if unwrap_eth:
            await async_sleep(5, 15, logs=False)
            await self.unwrap_eth()

    @check_gas
    async def unwrap_eth(self):
        logger.info(f"{self.account_id} | {self.address} | Unwrap ETH")

        balance_wei = (await self.get_balance(ZKSYNC_TOKENS['WETH']))['balance_wei']

        tx_data = await self.get_tx_data()

        tx = await self.weth_contract.functions.withdraw(balance_wei).build_transaction(tx_data)

        await self.execute_transaction(tx)