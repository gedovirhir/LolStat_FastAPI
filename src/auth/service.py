import bcrypt
from datetime import timedelta, datetime
from jose import jwt

from typing import Optional

from src.config import config
from src.database import DbSession
from src.user_service.models import User

from .enums import EXP
from .models import (UserRegister, 
                     UserBase,
                     Token
                     )
from .models import UserLoginData

def hash_password(password: str) -> bytes:
    """Generates a hashed version of the provided password."""
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)

def check_password(in_pass: str, check_hash: bytes) -> bool:
    return bcrypt.checkpw(in_pass.encode("utf-8"), check_hash)

def generate_jwt(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
        to_encode.update({EXP: expire})
    
    token = jwt.encode(
        to_encode, 
        config.auth.JWT_SECRET, 
        algorithm=config.auth.JWT_ALG
    )
    
    return token

async def register_user(user: UserRegister, session: DbSession):
    new_user = User(username=user.username)
    user_login_data = UserLoginData(
        email=user.email,
        password_hash=user.password,
        user=new_user
    )
    
    async with session.begin():
        session.add_all(
            [new_user, user_login_data]
        )

def generate_refresh_access(user: UserBase) -> dict:
    expires_delta = timedelta(minutes=config.auth.JWT_ACCESS_EXPIRES_MIN)
    data_to_encode = {'sub': user.email}
    
    token = {
        'access_token': generate_jwt(data_to_encode, expires_delta),
        'refresh_token': generate_jwt(data_to_encode)
    }
    
    return token

    