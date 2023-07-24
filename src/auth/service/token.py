from src.config import config

from ..models import (UserBase,
                     Token,
                     TokenData
                     )
# Стоит ли хранить и обрабатывать в токене exp если она в jwt проверяется автоматически
def generate_refresh_access(user: UserBase) -> Token:
    user_dict = UserBase.parse_obj(user).dict()
    access = TokenData(**user_dict, exp=config.auth.JWT_ACCESS_EXPIRES_MIN)
    refresh = TokenData(**user_dict, exp=config.auth.JWT_REFRESH_EXPIRES_MIN)
    
    token = Token.from_token_data(access=access, refresh=refresh)
    
    return token
