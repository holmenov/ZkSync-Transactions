from modules.account import Account
from utils.config import MINT_NFT_ABI
from utils.wrappers import check_gas


class MintNFT(Account):
    def __init__(self, account_id: int, private_key: str, proxy: str | None) -> None:
        super().__init__(account_id, private_key, proxy)

    @check_gas
    async def mint_nft(self, nft_contract: str):
        self.log_send('Mint NFT.')

        contract = self.get_contract(nft_contract, MINT_NFT_ABI)

        tx_data = await self.get_tx_data()

        tx = await contract.functions.mint().build_transaction(tx_data)

        await self.execute_transaction(tx)