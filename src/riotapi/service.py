import asyncio
from abc import (ABC, 
                 abstractmethod,
                 abstractproperty)

from typing import (List,
                    Optional,
                    NewType,
                    Any,
                    Dict,
                    Tuple,
                    Callable,
                    Coroutine)

from pydantic import parse_obj_as

from .models import MatchInfo, PlayerBaseInfo
from .types import Player_identity_field

from .models import (MatchResponse, 
                     MatchTimelineResponse, 
                     MatchInfo, 
                     PlayerBaseInfo, 
                     QueuePlayerStat
                     )
from .types import (Player_identity_field, 
                    Q_mode,
                    Tier,
                    Div,
                    Region,
                    Q_id
                    )

from .enums import PLAYER_IDENTITY_FIELDS, REGION

from .core import LolWatcher, lwatcher

MatchId = NewType('MatchId', str)

class AbstractConnector(ABC):
    _connector: Any
    _region: Region
    
    def __init__(self, connector: Any, region: Region):
        self._connector = connector
        self._region = region
    
    @property
    def connector(self):
        return self._connector
    
    @property
    def region(self):
        return self._region
    

class AbstractPlayerConnector(AbstractConnector):
    
    def get_identity_field(self, fields: Dict[Player_identity_field, str]) -> Tuple[Player_identity_field, str]:
        for k in fields:
            if k in PLAYER_IDENTITY_FIELDS:
                return (k, fields[k])
    
    @abstractmethod
    async def get_by_identity_field(self, **identity_field: Dict[Player_identity_field, str]) -> Optional[PlayerBaseInfo]: ...
    
    @abstractmethod
    async def get_matches(self) -> List[MatchId]: ...
    
    @abstractmethod
    async def get_league_entries(self, summoner_id: str, q_mode: Optional[Q_mode]) -> List[QueuePlayerStat]: ...
    
class AbstractMatchConnector(AbstractConnector):
    
    @abstractmethod
    async def get_match(self, match_id: MatchId, with_timeline: True) -> Optional[MatchInfo]: ...
    

class AbstractLeagueConnector(AbstractConnector):
    ###
    @abstractmethod
    async def get_entries(
        self, 
        queue: Q_mode,
        tier: Tier, 
        division: Div,
        page: int
    ) -> List[QueuePlayerStat]: ...
    
class AbstractManager(AbstractConnector):
    _player: AbstractPlayerConnector
    _match: AbstractMatchConnector
    _league: AbstractLeagueConnector
    
    @property
    def player(self):
        return self._player
    
    @property
    def match(self):
        return self._match
    
    @property
    def league(self):
        return self._league
    
    
class AbstractConnectorManager:
    
    def __init__(self): ...


### Доделать:
"""
Разделить функционал - почему get_player_entries лежит в модели player
Добавить внутренние классы - сделать чтобы в init инициализировался локальный класс плеера, который бы наследовался и в котором 
поле region = self._region
"""
def _a(func: Callable, *args, **kwargs):
    return asyncio.to_thread(func, *args, **kwargs)

class RiotPlayerConnector(AbstractPlayerConnector):
    _connector: LolWatcher
    
    def __init__(self, connector: LolWatcher, region: Region):
        super().__init__(connector, region)
        
        lwatcherSearchMethods = [
            self._connector.summoner.by_id,
            self._connector.summoner.by_name,
            self._connector.summoner.by_account,
            self._connector.summoner.by_puuid
        ]
        
        self._searchMethods = dict(zip(
            PLAYER_IDENTITY_FIELDS, lwatcherSearchMethods
        ))
        
    
    async def get_by_identity_field(self, **identity_field: Dict[Player_identity_field, str]) -> PlayerBaseInfo:
        id_f = self.get_identity_field(identity_field)
        if not id_f:
            raise TypeError(f'Missing identity field, pass the one of {",".join(PLAYER_IDENTITY_FIELDS)}')
        
        resp = await _a(self._searchMethods[id_f[0]], self._region, id_f[1])
        player = PlayerBaseInfo(**resp, region=self._region)
        
        return player
        
    
    async def get_matches(
        self,
        puuid: str,
        limit: int = None,
        offset: int = None,
        queue: Q_id = 420,
        #type: str = None,
        start_time: int = None,
        end_time: int = None
    ) -> List[MatchId]:
        
        matches = await _a(
            self._connector.match.matchlist_by_puuid,
            puuid = puuid,
            region = self._region,
            limit = limit,
            offset = offset,
            queue = queue,
            type = 'ranked',
            start_time = start_time,
            end_time = end_time, 
        )
        
        return matches

    async def get_league_entries(
        self, 
        summoner_id: str,
        q_mode: Optional[Q_mode] = None
    ):
        entries = await _a(
            self._connector.league.by_summoner,
            region=self._region,
            encrypted_summoner_id=summoner_id
        )
        entries = [e for e in entries if not e.update({REGION: self._region})]
        entries = parse_obj_as(List[QueuePlayerStat], entries)
        
        if q_mode:
            for e in entries:
                if e.q_mode == q_mode:
                    return e
        else:
            return entries

class RiotMatchConnector(AbstractMatchConnector):
    _connector: LolWatcher
    
    async def get_match(self, match_id: MatchId, with_timeline: True) -> MatchInfo:
        match_resp = await _a(
            self._connector.match.by_id,
            region=self._region,
            match_id=match_id
        )
        match_resp = MatchResponse.parse_obj(match_resp)
        timeline_resp = {}
        
        if with_timeline:
            timeline_resp = await _a(
                self._connector.match.timeline_by_match,
                region=self._region,
                match_id=match_id
            )
            timeline_resp = MatchTimelineResponse.parse_obj(timeline_resp)
        
        match_ = MatchInfo.combine(match_resp, timeline_resp)
        
        return match_

class RiotLeagueConnector(AbstractLeagueConnector):
    _connector: LolWatcher
    
    async def get_entries(
        self, 
        queue: Q_mode,
        tier: Tier, 
        division: Div,
        page: int
    ) -> List[QueuePlayerStat]:
        entries = await _a(
            self._connector.league.entries,
            queue=queue,
            tier=tier,
            division=division,
            page=page,
            region=self._region
        )
        
        entries = parse_obj_as(List[QueuePlayerStat], entries)
        
        return entries

class RiotManager(AbstractManager):
    
    def __init__(self, connector: LolWatcher, region: Region):
        super().__init__(connector, region)
        self._player = RiotPlayerConnector(connector, region)
        self._match = RiotMatchConnector(connector, region)
        self._league = RiotLeagueConnector(connector, region)
    
    @property
    def player(self):
        return self._player
    
    @property
    def match(self):
        return self._match
    
    @property
    def league(self):
        return self._league
    

RiotAPI = RiotManager(connector=lwatcher, region='ru')