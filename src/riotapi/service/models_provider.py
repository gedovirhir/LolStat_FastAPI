import asyncio

from typing import (List, 
                    Any,
                    Coroutine,
                    Callable,
                    Optional
                    )
from src.data_schemas.service import PlayerBaseInfo
from src.data_utils.service import AbstractMatch

from src.data_utils import AbstractPlayer, AbstractMatch
from src.data_schemas import MatchInfo, PlayerBaseInfo, QueuePlayerStat

from ..core import lwatcher
from ..types import Q_id

def __a(func: Callable):
    return asyncio.to_thread(func)

class RiotPlayer(PlayerBaseInfo, AbstractPlayer):
    _lwatcher = lwatcher
    
    
    
    async def get_info(self) -> PlayerBaseInfo:
        pass
    
    async def get_matches(
        self,
        queueId: Q_id = 420,
        start_time: Optional[int] = None, 
        end_time: Optional[int] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[AbstractMatch]:#Coroutine[Any, Any, List[AbstractMatch]]
        ############
        matches = self._lwatcher.match.matchlist_by_puuid(
            puuid=self.p,
            queue=queueId,
        )
        


def get_player_by_name(region: str, name: str):
    response = lwatcher.summoner.by_name(
        region=region,
        summoner_name=name
    )
    
    return response

def get_player_mathes(region: str, puuid: str):
    return lwatcher.match.matchlist_by_puuid(
        region=region,
        puuid=puuid
    )

def get_match(region: str, id: str):
    return lwatcher.match.by_id(
        region=region,
        match_id=id,
    )

def get_league_entries_players(
    region: str,
    tier: str,
    division: str,
    page: int,
    queue: str = 'RANKED_SOLO_5x5',
):
    return lwatcher.league.entries(
        region=region,
        queue=queue,
        tier=tier,
        division=division,
        page=page
    )