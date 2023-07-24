from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = Annotated[str, OAuth2PasswordBearer(tokenUrl="token")]
