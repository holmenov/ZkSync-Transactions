![ZkSync](https://i.imgur.com/rOVx6aD.png)

---

With this repository, you can do simple transactions on **ZkSync**. You can do actions such as:

- Send mail via Dmail.
- Wrap and unwrap ETH.
- Deposit and withdraw ETH on EraLend.
- Swap on SyncSwap.

## INSTALLATION

1. Install **Python 3.11+**.
2. `git clone https://github.com/holmenov/ZkSync-Transactions.git`.
3. `cd ZkSync-Transactions`.
4. `pip install -r requirements.txt`.
5. Paste your proxies into `proxy.txt` in `ip:port@login:password` format
6. Paste the wallet private key in `accounts.txt`.
7. Set the general settings in `settings.py`.
8. Set the routes settings in `modules_settings.py`.

## GENERAL SETTINGS

- `MAX_GAS` - Maximum GAS in GWEI for transactions [Integer].
- `GAS_MULTIPLAYER` - Multiplier for gas [Float].
- `RANDOM_WALLET` - Random wallet mode [Boolean].
- `REMOVE_WALLET` - Remove wallet after work [Boolean].
- `USE_PROXY` - Proxy mode [Boolean].
- `MAX_WORKERS` - Quantity threads [Integer].
- `WORKER_SLEEP_FROM`, `WORKER_SLEEP_TO` - Interval in seconds between thread starts [Integer].
- `SLEEP_AFTER_WORK_FROM`, `SLEEP_AFTER_WORK_TO` - Seconds to sleep after completing a task [Integer].
- `ZKSYNC_RPC` - RPC for ZkSync [String].
- `SLIPPAGE` - Percentage that is lost on exchange [Integer].

## MODULES SETTINGS

You can set different settings for each module.

- `min_amout` - Minimum amount in ETH.
- `max_amout` - Maximum amount in ETH.
- `decimal` - Number of decimal places to generate a random number in ETH.
- `all_amount` - Use a random % of your wallet balance.
- `min_percent` - Minimum percent of balance.
- `max_percent` - Maximum percent of balance.

There are also other settings that are individual to each module.