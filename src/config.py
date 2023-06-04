from pydantic import BaseSettings

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
    JWT_ACCESS_EXPIRES_MIN: int = 1800

class MainConfig(BaseSettings):
    LOG_LEVEL: str
    SECRET_KEY: str
    
    mongo = MongoConf()
    riot = RiotConf()
    postgres = PostgresConf()
    auth = AuthConf()

config = MainConfig()