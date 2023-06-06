from fastapi import (APIRouter, 
                     Depends,
                     HTTPException,
                     status
                     )

from sqlalchemy import select

from src.database import DbSession
from src.config import config

from .core import oauth2_scheme
from .enums import REGISTRATION_EMAIL_FAILED

from .models import UserRegister, Token
from .models import UserLoginData
from .service import (register_user,
                      generate_refresh_access)


router = APIRouter('/auth')

@router.post('/register', response_model=Token)
async def registrate_user(user: UserRegister, db: DbSession):
    user = await db.execute(
        select(UserLoginData).where(UserLoginData.email == user.email)
    )
    
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=REGISTRATION_EMAIL_FAILED
        )
    else:
        await register_user(user, db)
    
    return generate_refresh_access(user)

