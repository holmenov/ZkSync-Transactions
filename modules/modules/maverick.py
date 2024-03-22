import time
from modules.account import Account
from utils.config import MAVERICK_CONTRACTS, MAVERICK_POSITION_ABI, MAVERICK_ROUTER_ABI, ZERO_ADDRESS, ZKSYNC_TOKENS
from settings import MainSettings as SETTINGS
from utils.utils import async_sleep
from utils.wrappers import check_gas


class Maverick(Account):
    def __init__(self, account_id: int, private_key: str, proxy: str | None) -> None:
        super().__init__(account_id, private_key, proxy)
    
        self.swap_contract = self.get_contract(MAVERICK_CONTRACTS["router"], MAVERICK_ROUTER_ABI)
    
    async def get_min_amount_out(self, amount_wei: int, token_a_in: bool):
        contract = self.get_contract(MAVERICK_CONTRACTS["pool_information"], MAVERICK_POSITION_ABI)

        amount = await contract.functions.calculateSwap(
            self.w3.to_checksum_address(MAVERICK_CONTRACTS["pool"]),
            amount_wei,
            token_a_in,
            True,
            0
        ).call()

        return int(amount - (amount / 100 * SETTINGS.SLIPPAGE))

    def get_path(self, from_token: str, to_token: str):
        path_data = [
            self.w3.to_checksum_address(ZKSYNC_TOKENS[from_token]),
            self.w3.to_checksum_address(MAVERICK_CONTRACTS["pool"]),
            self.w3.to_checksum_address(ZKSYNC_TOKENS[to_token]),
        ]

        path = b"".join([bytes.fromhex(address[2:]) for address in path_data])

        return path

    async def swap_to_token(self, from_token: str, to_token: str, amount_wei: int):
        tx_data = await self.get_tx_data(value=amount_wei)

        deadline = int(time.time()) + 1000000

        min_amount_out = await self.get_min_amount_out(amount_wei, True)

        transaction_data = self.swap_contract.encodeABI(
            fn_name="exactInput",
            args=[(
                self.get_path(from_token, to_token),
                self.address,
                deadline,
                amount_wei,
                min_amount_out
            )]
        )

        refund_data = self.swap_contract.encodeABI(
            fn_name="refundETH",

        )

        contract_txn = await self.swap_contract.functions.multicall(
            [transaction_data, refund_data]
        ).build_transaction(tx_data)

        return contract_txn
    
    async def swap_to_eth(self, from_token: str, to_token: str, amount_wei: int):
        await self.approve(amount_wei, ZKSYNC_TOKENS[from_token], MAVERICK_CONTRACTS["router"])

        tx_data = await self.get_tx_data()

        deadline = int(time.time()) + 1000000

        min_amount_out = await self.get_min_amount_out(amount_wei, False)

        transaction_data = self.swap_contract.encodeABI(
            fn_name="exactInput",
            args=[(
                self.get_path(from_token, to_token),
                ZERO_ADDRESS,
                deadline,
                amount_wei,
                min_amount_out
            )]
        )

        unwrap_data = self.swap_contract.encodeABI(
            fn_name="unwrapWETH9",
            args=[
                0,
                self.address
            ]

        )

        contract_txn = await self.swap_contract.functions.multicall(
            [transaction_data, unwrap_data]
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
            self.log_send(f'{from_token} -> {to_token} | Swap on Maverick.')
            
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