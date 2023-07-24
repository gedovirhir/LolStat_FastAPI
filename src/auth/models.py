from datetime import datetime, timedelta

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

from typing import Optional, Union, NewType

from src.database import Base
from src.models import ProjectBase

from .service.crypt import (hash_password, 
                            check_password,
                            decode_jwt,
                            generate_jwt
                            )

Minutes = NewType('Minutes', int)

class UserLoginData(Base):
    __tablename__ = "user_login_data"
    
    user_id = Column(Integer, ForeignKey('user.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    
    email = Column(String(255), unique=True)
    password_hash = Column(LargeBinary)
    #created_at = Column(DateTime)   
    
    user = relationship('User', backref='login_data')
    
    def check_password(self, password: str):
        return check_password(password, self.password_hash)

class UserSessions(Base):
    __tablename__ = "user_sessions"
    
    user_login_data_id = Column(Integer, ForeignKey('user_login_data.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    refresh_token = Column(String(255))
    created_at = Column(DateTime)
    
class UserBase(ProjectBase):
    email: EmailStr

class UserPassword(UserBase):
    password: str 
    
class UserRegister(UserPassword):
    username: Optional[str]
    
    @validator('password', always=True)
    def hashing_password(cls, v):
        return hash_password(v)

class UserLogin(UserPassword):
    pass
        
        
class TokenData(UserBase):
    exp: Union[datetime, timedelta, Minutes]
    
    @validator('exp', pre=True, always=True)
    def convert_exp(cls, v):
        if isinstance(v, timedelta):
            return datetime.utcnow() + v
        elif isinstance(v, int):
            if len(str(v)) >= 10:
                return datetime.fromtimestamp(v)
            else:
                return datetime.utcnow() + timedelta(minutes=v)

        return v
    
    def is_expired(self):
        return datetime.utcnow() > self.exp
    
    @classmethod
    def from_token(cls, token: str):
        payload = decode_jwt(token)
        
        return cls.parse_obj(payload)

class Token(ProjectBase):
    access_token: Optional[str]
    refresh_token: Optional[str]
    
    @validator('access_token', 'refresh_token', always=True)
    def token_check(cls, value, values: dict):
        if values and not (value or [v[1] for v in values.items() if v[1]]):
            raise ValueError('At least one token must be passed')
    
        return value
    
    @classmethod
    def from_token_data(cls, access: Optional[TokenData] = {}, refresh: Optional[TokenData] = {}):
        t = {
            'access_token': generate_jwt(access.dict()),
            'refresh_token': generate_jwt(refresh.dict())
        }
        return cls.parse_obj(t)