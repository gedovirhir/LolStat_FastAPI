import asyncio
from typing import Any

from riotwatcher import LolWatcher

class AsyncLwatcher(LolWatcher):
    #######
    def __getattribute__(self, __name: str):
        print(__name)
        attr = super().__getattribute__(__name)
        if callable(attr):
            return AsyncMethodWrapper(attr)
        return attr

class AsyncMethodWrapper:
    def __init__(self, method):
        self.method = method

    async def __call__(self, *args, **kwargs):
        return await asyncio.to_thread(self.method, *args, **kwargs)
    