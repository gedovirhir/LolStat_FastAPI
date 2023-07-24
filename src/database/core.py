from sqlalchemy import Column, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import (AsyncEngine, 
                                    create_async_engine,
                                    AsyncSession,
                                    )

from fastapi import Depends, Request
from typing import Annotated, AsyncGenerator

from src.config import config

c = config.postgres

POSTGRES_URI = f"{c.POSTGRES_USER}:{c.POSTGRES_PASSWORD}@{c.POSTGRES_HOST}:{c.POSTGRES_PORT}/{c.POSTGRES_DB}"

ASYNC_SQLALCHEMY_URL = f"postgresql+asyncpg://{POSTGRES_URI}"
SYNC_SQLALCHEMY_URL = f"postgresql+psycopg2://{POSTGRES_URI}"

engine = create_async_engine(
    ASYNC_SQLALCHEMY_URL
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession, 
    expire_on_commit=False
)

class CustomBase:
    id = Column(Integer, primary_key=True)

Base = declarative_base(cls=CustomBase)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

async def get_autocommit_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            await session.close()
            raise e
            
DbSession = Annotated[AsyncSession, Depends(get_session)]
AutocommitSession = Annotated[AsyncSession, Depends(get_autocommit_session)]
