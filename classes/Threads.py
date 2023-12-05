from concurrent.futures import ThreadPoolExecutor
import random
import time
from typing import Callable

from settings import RANDOM_WALLETS, WORKER_SLEEP_FROM, WORKER_SLEEP_TO, MAX_WORKERS
from utils.utils import _async_run_module


class Threads:
    def __init__(self, data: list) -> None:
        self.data = data
        
        if RANDOM_WALLETS:
            random.shuffle(self.data)
    
    def start_workers(self, module: Callable, max_workers: int = MAX_WORKERS):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for account in self.data:
                executor.submit(
                    _async_run_module, module, account.get('id'), account.get('wallet'), account.get('address')
                )
                time.sleep(random.randint(WORKER_SLEEP_FROM, WORKER_SLEEP_TO))