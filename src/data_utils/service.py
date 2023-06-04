from abc import (ABC, 
                 abstractmethod,
                 abstractproperty)

from typing import (List,
                    Optional)

from src.riotapi.types import Q_mode, Region
from src.data_schemas.service import (QueuePlayerStat,
                                      PlayerBaseInfo,
                                      MatchInfo)

class AbstractMatch(ABC):
    
    def __init__(self, match_id: str) -> None:
        self._match_id = match_id
        
    @abstractmethod
    async def get_info(self) -> MatchInfo:
        """
        Do functuion to collect data from f.e. MongoDB or RiotAPI
        """
        pass
    
    # Внутри будет модель pydantic с авто полями для удобного доступа а этот оборачивающий класс будет использоваться для статистики и прочих высшых функций
    """@abstractmethod
    async def get_some_statistic(): ..."""
    
class  AbstractPlayer(ABC):
    
    def __init__(
        self, 
        summonerId: Optional[str] = None, 
        name: Optional[str] = None,
        region: Region = 'ru'
    ):
        ##############
        if not (summonerId or name):
            raise ValueError("No name of summonerId specified")
        
        self._summonerId = summonerId
        self._name = name
        self._region = region
        
    @abstractmethod
    async def get_info(self) -> PlayerBaseInfo: ...
        
    @abstractmethod
    async def get_matches(self) -> List[AbstractMatch]: ...
    
    @abstractmethod
    async def get_stat(self, queue: Q_mode) -> QueuePlayerStat: ...

