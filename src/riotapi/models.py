from typing import (Optional, 
                    Union,
                    Dict,
                    List,
                    Any)

from pydantic import (Extra,
                      validator,
                      root_validator
                    )
from pydantic.fields import ModelField

from src.riotapi.types import (Q_mode,
                               Div,
                               Tier,
                               Region)
from src.models import ProjectBase, AutoSerialized

from .enums import *

class RegionMixin(ProjectBase):
    region: Region = Region.ru   

class QueuePlayerStat(AutoSerialized, RegionMixin):
    leagueId: str
    summonerId: str
    
    queueType: Q_mode
    tier: Tier
    division: Div
    
    wins: int
    losses: int
    
    class Config:
        extra = Extra.allow
    
    @root_validator(pre=True)
    def convert_rank_to_division(cls, values: dict):
        if values.get('rank') and not values.get('division'):
            values.update(
                {'division': values.pop('rank')}
            )
            
        return values


class MatchBase(ProjectBase):
    class MetadataInfo(AutoSerialized):
        matchId: str
        participants: List[str]
    
    metadata: MetadataInfo
    
class MatchTimelineResponse(MatchBase):
    class TimelineInfo(AutoSerialized):
        frameInterval: int
        frames: list
    
    info: TimelineInfo

class MatchResponse(MatchBase):
    class GameInfo(AutoSerialized):
        gameId: str
        queueId: int
        platformId: str
    
    info: GameInfo
 
class MatchInfo(MatchBase, RegionMixin):
    info: Optional[MatchResponse.GameInfo]
    timeline: Optional[MatchTimelineResponse.TimelineInfo] 
    
    @classmethod
    def combine(cls, match_info: Optional[MatchResponse], timeline: Optional[MatchTimelineResponse]):
        to_combine = [match_info, timeline]
        combined = {}
        
        for o in to_combine:
            if o:
                combined.update(o.dict())
                
        return cls.parse_obj(combined)
 
class PlayerBaseInfo(AutoSerialized, RegionMixin):
    accountId: Optional[str]
    puuid: Optional[str]
    summonerId: Optional[str]
    name: Optional[str]
        
    @classmethod
    def get_identify_field(cls, values: dict) -> tuple:
        for f in PLAYER_IDENTITY_FIELDS:
            if values.get(f):
                return (f, values[f])
    
    @property
    def identity_field(self):
        field = self.get_identify_field(self.dict())
        
        return field
    
    @root_validator(pre=True)
    def convert_id_to_summonerId(cls, values: dict):
        if values.get(ID) and not values.get(SUMMONERID):
            values.update(
                {SUMMONERID: values.pop(ID)}
            )
        return values
        
    @root_validator
    def check_id_info(cls, values: dict):
        if not (
            cls.get_identify_field(values)
        ):
            raise ValueError('At least one identify field must be defined')
        return values
