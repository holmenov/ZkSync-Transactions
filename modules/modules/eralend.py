from settings import MainSettings as SETTINGS
from modules.account import Account
from utils.config import ERALEND_ABI, ERALEND_CONTRACTS
from utils.utils import async_sleep
from utils.wrappers import check_gas


class Eralend(Account):
    def __init__(self, account_id: int, private_key: str, proxy: str | None) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        
        self.eraland_contract = self.get_contract(ERALEND_CONTRACTS['landing'], ERALEND_ABI)
        
    async def get_deposit_amount(self):
        amount = await self.eraland_contract.functions.balanceOfUnderlying(self.address).call()
        return amount
    
    @check_gas
    async def deposit(
        self,
        min_amount: int,
        max_amount: int,
        decimal: int,
        all_amount: bool,
        min_percent: int,
        max_percent: int,
        make_withdraw: bool
    ):
        self.log_send('Make deposit on Eralend.')
        
        if all_amount:
            amount_wei, _ = await self.get_percent_amount('ETH', min_percent, max_percent)
        else:
            amount_wei, _ = await self.get_random_amount('ETH', min_amount, max_amount, decimal)
        
        tx = await self.get_tx_data(value=amount_wei)
        
        tx.update({'to': self.w3.to_checksum_address(ERALEND_CONTRACTS['landing']), 'data': '0x1249c58b'})
        
        await self.execute_transaction(tx)
        
        if make_withdraw:
            await async_sleep(SETTINGS.LANDINGS_SLEEP[0], SETTINGS.LANDINGS_SLEEP[1], logs=False)
            await self.withdraw()
    
    @check_gas
    async def withdraw(self):
        self.log_send('Make withdraw from Eralend.')
        
        tx_data = await self.get_tx_data()
        
        amount = await self.get_deposit_amount()

        tx = await self.eraland_contract.functions.redeemUnderlying(amount).build_transaction(tx_data)
        
        await self.execute_transaction(tx)