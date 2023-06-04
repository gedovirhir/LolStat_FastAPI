from typing import (Optional, 
                    Union,
                    Dict,
                    List,
                    Any)

from pydantic import (BaseModel,
                      Extra,
                      validator,
                      root_validator
                    )
from pydantic.fields import ModelField
from abc import ABC

from src.riotapi.types import (Q_mode,
                               Div,
                               Tier)

class AutoSerialized(BaseModel):
    class Config:
        extra = Extra.allow
    
    def __init__(self, **data):
        super().__init__(**data)
        for key, value in data.items():
            if key not in self.__fields__:
                setattr(self, key, self.__auto_serialize(value))
    
    def __auto_serialize(self, data: Union[Dict[str, Any], List[Any], Any]):
        if isinstance(data, dict):
            return AutoSerialized(**data)
        
        elif isinstance(data, list):
            for i, item in enumerate(data):
                data[i] = self.__auto_serialize(item)
            return data
        
        else:
            return data
        

class QueuePlayerStat(AutoSerialized):
    q_mode: Q_mode
    tier: Tier
    division: Div
    
    total_games: int
    wins: int = None
    loses: int = None
    
    class Config:
        extra = Extra.allow
    
    __wl_enum = ('wins', 'loses')
        
    @validator(*__wl_enum, pre=False, always=True)
    def wins_and_loses_calculate(cls, value, values: dict, field: ModelField):
        if value:
            return value
        
        f_i = cls.__wl_enum.index(field.name)
        field_name_2 = cls.__wl_enum[1 - f_i]
        value_2 = values.get(field_name_2)
        
        if value_2:
            return values['total_games'] - value_2
        else:
            raise ValueError("Both wins and loses cannot be None")
    
    @validator(*__wl_enum, pre=False)
    def wins_and_loses_validate(cls, value, values: dict, field: ModelField):
        if value > values['total_games']: 
            raise ValueError(f"{field.name} > total_games")


class PlayerBaseInfo(AutoSerialized):
    accountId: Optional[str]
    puuid: Optional[str]
    summoner_id: Optional[str]
    name: Optional[str]
    
    class Config:
        extra = Extra.allow
        
    @root_validator
    def check_id_info(cls, values):
        if not (
            values.get('accountId')
            or values.get('puuid')
            or values.get('summoner_id')
            or values.get('name')
        ):
            raise ValueError('At least one identify field must be defined')
        return values
        
class MatchInfo(AutoSerialized):
    
    class MetadataInfo(AutoSerialized):
        matchId: str
        participants: List[str]
        
        class Config:
            extra = Extra.allow
    
    class GameInfo(AutoSerialized):
        gameId: str
        queueId: int
        platformId: str
        
        class Config:
            extra = Extra.allow
            
    metadata: MetadataInfo
    info: GameInfo