from modules.account import Account


class BalanceChecker(Account):
    def __init__(self, account_id: int, private_key: str, proxy: str | None) -> None:
        super().__init__(account_id, private_key, proxy)
    
    async def check_balance(self):
        try:
            balance, _ = await self.get_balance()
            
            self.log_send(f'Current balance: {round(balance, 6)} $ETH.', self.account_id, self.address)
            
            return balance
        
        except Exception as error:
            self.log_send(f'Error when balance checking: {error}', self.account_id, self.address, status='error')
            return False