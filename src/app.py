from fastapi import FastAPI
import uvicorn

"""from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
"""
from .config import config

app = FastAPI()

from src.auth import router as auth_router
from src.swagger import router as swagger_router
from src.lol_service import lol_router
from src.mongo.core import matches

app.include_router(auth_router)
app.include_router(swagger_router)
app.include_router(lol_router)

"""@app.on_event("startup")
async def on_startup() -> None:
    redis_cache = RedisBackend(f"redis://:{config.redis.REDIS_PASSWORD}@{config.redis.REDIS_HOST}:6379")
    FastAPICache.init(backend=redis_cache, prefix="fastapi-cache")"""