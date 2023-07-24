from typing import Optional, Dict, Union, List, TypeVar, Coroutine, Any

from pydantic import parse_obj_as

from src.riotapi.models import PlayerBaseInfo, QueuePlayerStat, MatchInfo
from src.riotapi.types import Div, Player_identity_field, Q_mode, Q_id, Tier, Region

from .core import motor_db, MongoClient, Collection
from .enums import (PLAYERS, 
                    MATCHES,
                    LEAGUE_ENTRIES)

from src.riotapi.service import (AbstractConnector,
                                 AbstractPlayerConnector,
                                 AbstractMatchConnector,
                                 AbstractLeagueConnector,
                                 AbstractManager, MatchId
                                 )


InsertData = TypeVar('InsertData', List[dict], dict)

async def __insert_objects(col_name: str, data: InsertData):
    coll = motor_db[col_name]
    if isinstance(data, list):
        await coll.insert_many(data)
    else:
        await coll.insert_one(data)

async def insert_player(data: InsertData):
    return await __insert_objects(PLAYERS, data)

async def insert_match(data: InsertData):
    return await __insert_objects(MATCHES, data)

async def insert_ranked_player(data: InsertData):
    return await __insert_objects(LEAGUE_ENTRIES, data)


class MongoPlayerConnector(AbstractPlayerConnector):
    _connector: MongoClient
    
    @property
    def _player_connector(self) -> Collection:
        return self._connector[PLAYERS]
    
    @property
    def _matches_connector(self) -> Collection:
        return self._connector[MATCHES]
    
    @property
    def _league_connector(self) -> Collection:
        return self._connector[LEAGUE_ENTRIES]
    
    
    async def get_by_identity_field(self, **identity_field: Dict[Player_identity_field, str]) -> Optional[PlayerBaseInfo]:
        id_f = self.get_identity_field(identity_field)
        
        player = await self._player_connector.find_one(
            {id_f[0]: id_f[1]}
        )
        if player:
            return PlayerBaseInfo.parse_obj(player)
    
    async def get_matches(
        self,
        puuid: str,
        limit: int = 0,
        offset: int = 1000,
        queue: Q_id = 420,
        #type: str = None,
        start_time: int = None,
        end_time: int = None
    
    ) -> List[MatchInfo]:
        filter = {'metadata.participants': puuid, 'info.queueId': queue}
        
        if start_time or end_time:
            date_filter = {'info.gameCreation': {}}
            if start_time: date_filter['info.gameCreation'].update({"$gte": start_time})
            if end_time: date_filter['info.gameCreation'].update({"$lte": end_time})
            
            filter.update(date_filter)
        
        matches = self._matches_connector.find(
            filter,
            skip=offset,
            limit=limit
        )
        
        matches = await matches.to_list(length=None)
        
        return parse_obj_as(List[MatchInfo], matches)
    
    async def insert_player(self, player: Union[List[PlayerBaseInfo], PlayerBaseInfo]):
        await insert_player(player.dict())
    
    async def get_league_entries(self, summoner_id: str, q_mode: Optional[Q_mode] = None) -> List[QueuePlayerStat]:
        filters = {
            "summonerId": summoner_id
        }
        if q_mode: filters.update({'queueType': q_mode})
        
        entries = self._league_connector.find(
            filters
        )
        
        entries = await entries.to_list(length=None)
        
        return parse_obj_as(List[QueuePlayerStat], entries)

    
    
class MongoMatchConnector(AbstractMatchConnector):
    _connector: MongoClient
    
    @property
    def _matches_connector(self) -> Collection:
        return self._connector[MATCHES]

    async def get_match(self, match_id: MatchId) -> Optional[MatchInfo]:
        match = await self._matches_connector.find_one(
            {"metadata.matchId": match_id}
        )
        
        return MatchInfo.parse_obj(match) if match else None
    
    async def insert_match(self, match: Union[List[MatchInfo], MatchInfo]):
        await insert_match(match.dict())
    
    async def get_aggregation(self, stages_pipeline: List[dict]): 
        aggr = self._matches_connector.aggregate(stages_pipeline)
        res = await aggr.to_list(length=None)
        
        return res
        

class MongoLeagueConnector(AbstractLeagueConnector):
    _connector: MongoClient
    _page_size: int = 50
    
    @property
    def _league_connector(self) -> Collection:
        return self._connector[LEAGUE_ENTRIES]
    
    async def get_entries(
        self, 
        page: int,
        queue: Optional[Q_mode] = None, 
        tier: Optional[Tier] = None, 
        division: Optional[Div] = None, 
    ) -> List[QueuePlayerStat]:
        filters = {
            "queueType": queue,
            "tier": tier,
            "division": division,
        }
        filters = { k:v for k,v in filters.items() if v} 
        
        offset = self._page_size * page
        limit = self._page_size
        
        entries = self._league_connector.find(
            filters,
            skip=offset,
            limit=limit
        )
        
        entries = await entries.to_list(length=None)
        
        return parse_obj_as(List[QueuePlayerStat], entries)

    async def insert_entries(self, entries: Union[List[QueuePlayerStat], QueuePlayerStat]):
        await insert_ranked_player(entries)
        
class MongoManager(AbstractManager):
    
    def __init__(self, connector, region: Region):
        super().__init__(connector, region)
        self._player = MongoPlayerConnector(connector, region)
        self._match = MongoMatchConnector(connector, region)
        self._league = MongoLeagueConnector(connector, region)
    
    @property
    def player(self):
        return self._player
    
    @property
    def match(self):
        return self._match
    
    @property
    def league(self):
        return self._league    


RiotMongo = MongoManager(connector=motor_db, region='ru')