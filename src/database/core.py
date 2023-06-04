from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import (AsyncEngine, 
                                    async_sessionmaker, 
                                    create_async_engine,
                                    AsyncSession,
                                    )

from fastapi import Depends, Request
from typing import Annotated, AsyncGenerator

from src.config import config

c = config.postgres
POSTGRES_URI = f"postgresql+asyncpg://{c.POSTGRES_USER}:{c.POSTGRES_PASSWORD}@{c.POSTGRES_HOST}:{c.POSTGRES_PORT}/{c.POSTGRES_DB}"

engine = create_async_engine(
    POSTGRES_URI
)

SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

class CustomBase:
    id = Column(Integer, primary_key=True)

Base = declarative_base(cls=CustomBase)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

DbSession = Annotated[AsyncSession, Depends(get_db)]
