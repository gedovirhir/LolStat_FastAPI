import os
from pydantic import BaseSettings

from typing import Optional

ENV_FILE = '.env'

class BaseConf(BaseSettings):
    class Config:
        env_file=ENV_FILE

class MongoConf(BaseConf):
    MONGO_HOST: str = 'localhost'
    MONGO_PORT: int = 27017
    MONGO_DB_NAME: str 
    
class RiotConf(BaseConf):
    RIOT_API_KEY: str
    
class PostgresConf(BaseConf):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

class AuthConf(BaseConf):
    JWT_SECRET: str
    JWT_ALG: str = 'HS256'
    JWT_ACCESS_EXPIRES_MIN: int = 300
    JWT_REFRESH_EXPIRES_MIN: int = 60*24*30

class RedisConf(BaseConf):
    REDIS_HOST: str = '127.0.0.1'
    REDIS_PASSWORD: Optional[str] = None
    

class MainConfig(BaseConf):
    LOG_LEVEL: str
    SECRET_KEY: str
    
    mongo = MongoConf()
    riot = RiotConf()
    postgres = PostgresConf()
    redis = RedisConf()
    auth = AuthConf()

config = MainConfig()
