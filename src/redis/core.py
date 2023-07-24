import redis
from fastapi import Depends

from typing import Annotated

from src.config import config

__c = config.redis

c_pool = redis.ConnectionPool(
    host=__c.REDIS_HOST,
    password=__c.REDIS_PASSWORD,
    db=0,
    decode_responses=True,
    
)
def get_rs_conn():
    return redis.Redis(connection_pool=c_pool, 
                       decode_responses=True)

class rs_conn_handler:
    def __getattr__(self, __name: str):
        conn = get_rs_conn()
        return getattr(conn, __name)
    def __getattribute__(self, __name: str):
        conn = get_rs_conn()
        return conn.__getattribute__(__name)

rs_conn: redis.Redis = rs_conn_handler()

async def get_redis_session(): # db=1??
    try:
        session = get_rs_conn()
        yield session
    
    finally:
        session.close()

RedisSession = Annotated[redis.Redis, Depends(get_redis_session)]