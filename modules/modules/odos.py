from modules.account import Account
from settings import MainSettings as SETTINGS
from utils.config import ODOS_CONTRACT, ZERO_ADDRESS, ZKSYNC_TOKENS
from utils.utils import async_sleep
from utils.wrappers import check_gas


class Odos(Account):
    def __init__(self, account_id: int, private_key: str, proxy: str | None) -> None:
        super().__init__(account_id, private_key, proxy)
        
        self.headers = {"Content-Type": "application/json"}

    async def quote(self, from_token: str, to_token: str, amount_wei: int):
        url = "https://api.odos.xyz/sor/quote/v2"

        request_body = {
            "chainId": self.chain_id,
            "inputTokens": [
                {
                    "tokenAddress": self.w3.to_checksum_address(from_token),
                    "amount": f"{amount_wei}"
                }
            ],
            "outputTokens": [
                {
                    "tokenAddress": self.w3.to_checksum_address(to_token),
                    "proportion": 1
                }
            ],
            "slippageLimitPercent": SETTINGS.SLIPPAGE,
            "userAddr": self.address,
            "referralCode": 0,
            "compact": True
        }

        response_data = await self.make_request(method='POST', url=url, headers=self.headers, json=request_body)
        
        return response_data
    
    async def assemble(self, path_id):
        url = "https://api.odos.xyz/sor/assemble"

        request_body = {
            "userAddr": self.address,
            "pathId": path_id,
            "simulate": False,
        }
        
        response_data = await self.make_request(method='POST', url=url, headers=self.headers, json=request_body)

        return response_data
    
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
            self.log_send(f'{from_token} -> {to_token} | Swap on Odos.')

            if all_amount:
                amount_wei, _ = await self.get_percent_amount(from_token, min_percent, max_percent)
            else:
                amount_wei, _ = await self.get_random_amount(from_token, min_amount, max_amount, decimal)

            from_token_addr = ZERO_ADDRESS if from_token == "ETH" else ZKSYNC_TOKENS[from_token]
            to_token_addr = ZERO_ADDRESS if to_token == "ETH" else ZKSYNC_TOKENS[to_token]

            if from_token_addr != ZERO_ADDRESS:
                await self.approve(amount_wei, from_token_addr, self.w3.to_checksum_address(ODOS_CONTRACT["router"]))

            quote_data = await self.quote(from_token_addr, to_token_addr, amount_wei)

            transaction_data = await self.assemble(quote_data["pathId"])

            transaction = transaction_data["transaction"]

            tx_data = await self.get_tx_data()
            tx_data.update(
                {
                    "to": self.w3.to_checksum_address(transaction["to"]),
                    "data": transaction["data"],
                    "value": int(transaction["value"]),
                }
            )

            tx_status = await self.execute_transaction(tx_data)

            if swap_reverse:
                await async_sleep(5, 15, logs=False)
                await self.swap(to_token, from_token, 0.01, 0.01, decimal, True, 100, 100, False)
            else:
                return tx_status
        
        except Exception as e:
            self.log_send(f'Error in module «{__class__.__name__}»: {e}', status='error')
            return False