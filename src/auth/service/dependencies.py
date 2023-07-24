from fastapi import Depends, HTTPException, Query, Body
from typing import Annotated, Union, Optional

from src.database import DbSession

from ..core import oauth2_scheme
from ..models import TokenData, UserBase, UserLogin, UserLoginData
from .crypt import JWTError
from .user import get_user

# class CurrentUser

async def verify_token(token: oauth2_scheme) -> TokenData:
    """
    Decode token and return token payload
    Args:
        token (oauth2_scheme): _description_
    """
    
    try:
        payload = TokenData.from_token(token)
        
        return payload
        
    except JWTError as e:
        raise HTTPException(
            401,
            f'JWT error: {e}'
        )

verified_token = Annotated[TokenData, Depends(verify_token)]

async def get_current_user(
    token_data: verified_token,
    db: DbSession
):
    user = await get_user(token_data, db)
    if not user:
        raise HTTPException(
            404,
            "User not found"
        )
    
    return user

current_user = Annotated[UserLoginData, Depends(get_current_user)]

async def authorization_user(
    login_data: UserLogin,
    db: DbSession
):
    try:
        db_user_ = await get_user(login_data, db)

        assert db_user_
        assert db_user_.check_password(login_data.password)
    except ConnectionRefusedError:
        raise HTTPException(
            500,
            'Internal server error'
        )
    except Exception as e:
        raise HTTPException(
            401,
            'Incorrect creditails'
        )

authorize_user = Annotated[None, Depends(authorization_user)]