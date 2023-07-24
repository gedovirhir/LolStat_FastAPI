from sqlalchemy import (Column,
                        String
                        )
from sqlalchemy.orm import relationship

from src.database import Base

class User(Base):
    __tablename__ = "user"
    
    username = Column(String(255))
