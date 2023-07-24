from pydantic import BaseModel


from sqlalchemy import (Column,
                        String,
                        Integer,
                        ForeignKey,
                        UniqueConstraint
                        )
from sqlalchemy.orm import relationship 

from typing import List

from src.riotapi.types import Region
from src.database import Base
from src.models import ProjectBase

from src.riotapi.models import QueuePlayerStat

class UserLolProfile(Base):
    __tablename__ = "user_lol_profile"
    
    user_id = Column(Integer, ForeignKey('user.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    puuid = Column(String(255))
        
    user = relationship('User', backref='lol_profile')
    
    __table_args__ = (UniqueConstraint('user_id', 'puuid'),)


class PostProfile(ProjectBase):
    region: Region
    name: str

class ResponseProfile(ProjectBase):
    name: str
    summonerLevel: str
    league_entries: List[QueuePlayerStat]
