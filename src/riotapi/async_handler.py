import asyncio

from requests import HTTPError
from riotwatcher import LolWatcher

from .core import lwatcher

class AsyncLolWatcher:
    
    __lwatcher = lwatcher

    @classmethod
    @property
    def _lwatcher(cls):
        return cls.__lwatcher
    

class player:
    def __init__(
        self,
        id: str,
        lwatcher: LolWatcher = lwatcher,
        info: dict = None 
    ):
        self._id = id
        self._lwatcher = lwatcher
        self._info = info 
        self._ranked_info = None
    def __repr__(self) -> str:
        return str(self.info)
    
    def __getattr__(self, __name: str):
        return self._info[__name]

    def _set_ranked_info(self):
        self._ranked_info = self._lwatcher.league.by_summoner(
            self._info['region'],
            self._id
        )
    
    def _set_total_wins(self):
        pass

    @property
    def id(self):
        return self._id
    
    @property
    def info(self):
        return self._info
    
    @property
    def ranked_info(self):
        if not self._ranked_info:
            self._set_ranked_info()
        return self._ranked_info
    

"""lhd = LolHandler(
    "RGAPI-6fcb3735-b220-443c-b524-4a9bbf7a1bf4"
)

plr = lhd.get_players_by(
    'ru',
    name='gedovirhir'
)[0]

print(plr.info)"""
