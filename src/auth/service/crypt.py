from jose import jwt, JWTError
import bcrypt

from src.config import config

def hash_password(password: str) -> bytes:
    """Generates a hashed version of the provided password."""
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)

def check_password(in_pass: str, check_hash: bytes) -> bool:
    return bcrypt.checkpw(in_pass.encode("utf-8"), check_hash)

class JWTContext:
    
    def __init__(
        self,
        secret,
        algorithm: str,
    ):
        self.secret = secret
        self.algorithm = algorithm
    
    def encode(self, *args, **kwargs):
        return jwt.encode(
            key=self.secret,
            algorithm=self.algorithm,
            *args, **kwargs
        )
    
    def decode(self, *args, **kwargs):
        return jwt.decode(
            key=self.secret,
            algorithms=self.algorithm,
            *args, **kwargs
        )

jwt_context = JWTContext(
    secret=config.auth.JWT_SECRET,
    algorithm=config.auth.JWT_ALG
)    

def generate_jwt(data: dict) -> str:
    return jwt_context.encode(data)

def decode_jwt(token: str) -> dict:
    return jwt_context.decode(token)