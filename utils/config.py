import json


with open('data/rpc.json', 'r') as file:
    RPC = json.load(file)
    
with open('data/erc20_abi.json', 'r') as file:
    ERC20_ABI = json.load(file)
    
with open('data/dmail/abi.json', 'r') as file:
    DMAIL_ABI = json.load(file)
    
with open('accounts.txt', 'r') as file:
    ACCOUNTS = [row.strip() for row in file]
    
with open("proxy.txt", "r") as file:
    PROXIES = [row.strip() for row in file]
    
with open("data/eralend/abi.json", "r") as file:
    ERALEND_ABI = json.load(file)
    
with open("data/syncswap/router.json", "r") as file:
    SYNCSWAP_ROUTER_ABI = json.load(file)

with open('data/syncswap/classic_pool.json', "r") as file:
    SYNCSWAP_CLASSIC_POOL_ABI = json.load(file)

with open('data/syncswap/classic_pool_data.json', "r") as file:
    SYNCSWAP_CLASSIC_POOL_DATA_ABI = json.load(file)

with open('data/weth/abi.json', "r") as file:
    WETH_ABI = json.load(file)

with open('data/mint_nft/abi.json', "r") as file:
    MINT_NFT_ABI = json.load(file)

with open('data/rubyscore/abi.json', "r") as file:
    RUBYSCORE_ABI = json.load(file)

with open('data/owlto/abi.json', "r") as file:
    OWLTO_ABI = json.load(file)

with open('data/maverick/position.json', "r") as file:
    MAVERICK_POSITION_ABI = json.load(file)

with open('data/maverick/router.json', "r") as file:
    MAVERICK_ROUTER_ABI = json.load(file)

with open('data/mute/router.json', "r") as file:
    MUTE_ROUTER_ABI = json.load(file)

MAX_APPROVE = 2**256 - 1

ETH_MASK = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"

DMAIL_CONTRACT = '0x981F198286E40F9979274E0876636E9144B8FB8E'

OWLTO_CONTRACT = '0xD48e3caf0D948203434646a3f3e80f8Ee18007dc'

INCH_CONTRACT = {
    "router": "0x1111111254eeb25477b68fb85ed929f73a960582",
}

ODOS_CONTRACT = {
    "router": "0x4bba932e9792a2b917d47830c93a9bc79320e4f7",
}

MUTE_CONTRACTS = {
    "router": "0x8B791913eB07C32779a16750e3868aA8495F5964"
}

MAVERICK_CONTRACTS = {
    "router": "0x39E098A153Ad69834a9Dac32f0FCa92066aD03f4",
    "pool": "0x41C8cf74c27554A8972d3bf3D2BD4a14D8B604AB",
    "pool_information": "0x57D47F505EdaA8Ae1eFD807A860A79A28bE06449",
}

RUBYSCORE_CONTRACTS = {
    "vote": "0xCb84d512F0C9943D3BC6B4Be8801aC8Aa6621a54",
}

ERALEND_CONTRACTS = {
    "landing": "0x22d8b71599e14f20a49a397b88c1c878c86f5579",
    "collateral": "0xc955d5fa053d88e7338317cc6589635cd5b2cf09"
}

SYNCSWAP_CONTRACTS = {
    "router": "0x2da10A1e27bF85cEdD8FFb1AbBe97e53391C0295",
    "classic_pool": "0xf2DAd89f2788a8CD54625C60b55cD3d2D0ACa7Cb"
}

ZKSYNC_TOKENS = {
    "ETH": "0x5aea5775959fbc2557cc8789bc1bf90a239d9a91",
    "WETH": "0x5aea5775959fbc2557cc8789bc1bf90a239d9a91",
    "USDC": "0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4",
    "USDT": "0x493257fd37edb34451f62edf8d2a0c418852ba4c",
    "BUSD": "0x2039bb4116b4efc145ec4f0e2ea75012d6c0f181",
    "MATIC": "0x28a487240e4d45cff4a2980d334cc933b7483842",
    "OT": "0xd0ea21ba66b67be636de1ec4bd9696eb8c61e9aa",
    "MAV": "0x787c09494ec8bcb24dcaf8659e7d5d69979ee508",
    "WBTC": "0xbbeb516fb02a01611cbbe0453fe3c580d7281011",
}