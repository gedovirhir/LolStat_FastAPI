from sqlalchemy import (Column,
                        String,
                        Integer,
                        ForeignKey,
                        LargeBinary,
                        DateTime
                        )
from sqlalchemy.orm import relationship

from pydantic import BaseModel, validator
from pydantic.networks import EmailStr

from typing import Optional

from src.database import Base
from src.models import ProjectBase

from .service import (hash_password,
                      check_password)

class UserLoginData(Base):
    __tablename__ = "user_login_data"
    
    user_id = Column(Integer, ForeignKey('user.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    
    email = Column(String(255), unique=True)
    password_hash = Column(LargeBinary)
    #created_at = Column(DateTime)   
    
    user = relationship('User', backref='login_data')
    
    def check_password(self, password):
        return check_password(password, self.password_hash)


class UserBase(ProjectBase):
    email: EmailStr
    username: Optional[str]

class UserRegister(UserBase):
    password: str 
    
    @validator('password', always=True)
    def hashing_password(cls, v):
        return hash_password(v)

class UserLogin(UserBase):
    password: str

class Token(ProjectBase):
    access_token: str
    refresh_token: str
