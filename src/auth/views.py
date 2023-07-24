from datetime import timedelta

from fastapi import (APIRouter, 
                     Depends,
                     HTTPException,
                     status
                     )

from src.database import DbSession, AutocommitSession
from src.config import config

from src.user_service.models import User

from typing import Annotated

from .core import oauth2_scheme
from .enums import REGISTRATION_EMAIL_FAILED

from .models import (UserBase, 
                     UserRegister,
                     UserLogin, 
                     Token,
                     TokenData
                     )
from .models import UserLoginData

from .service.user import (get_user, 
                           register_user,
                           )
from .service.token import (generate_refresh_access
                            )
from .service.dependencies import (verified_token,
                                   current_user,
                                   authorize_user,
                                   authorization_user
                      )

router = APIRouter(prefix='/auth')

@router.post('/register', response_model=Token)
async def post_registrate_user(user: UserRegister, db: AutocommitSession):
    db_user = await get_user(user, db)
    
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=REGISTRATION_EMAIL_FAILED
        )
    else:
        await register_user(user, db)
    
    return generate_refresh_access(user)

jwt_router = APIRouter(prefix='/jwt')

@jwt_router.post(
    '/token', 
    response_model=Token,
    dependencies=[Depends(authorization_user)]
)
async def post_login_for_token(
    login_data: UserLogin
): 
    t = generate_refresh_access(login_data)
    return t

@jwt_router.get(
    '/refresh', 
    response_model=Token
)
async def get_jwt_refresh(token: verified_token):
    t = generate_refresh_access(token)
    
    return t

# @router.get('/check_access')
async def get_check_access(user: current_user):
    user_e = user.email
    
    return {'status': 200, 'email': user_e}

