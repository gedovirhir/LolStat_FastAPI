from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.user_service.models import User

from ..models import (UserBase, 
                     UserRegister, 
                     UserLogin,
                     )
from ..models import UserLoginData

async def get_user(user: UserBase, session: AsyncSession) -> Optional[UserLoginData]:
    db_user = await session.execute(
        select(UserLoginData).where(UserLoginData.email == user.email)
    )
    db_user = db_user.first()
    db_user = db_user[0] if db_user else db_user
    
    return db_user

async def register_user(user: UserRegister, session: AsyncSession):
    new_user = User(username=user.username)
    user_login_data = UserLoginData(
        email=user.email,
        password_hash=user.password,
        user=new_user
    )
    
    session.add_all(
        [new_user, user_login_data]
    )
    