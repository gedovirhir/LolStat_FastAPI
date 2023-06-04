from typing import Union, List, TypeVar

from .core import db
from .enums import (PLAYERS, 
                    MATCHES,
                    RANKED_PLAYERS)

InsertData = TypeVar('InsertData', List[dict], dict)

async def __insert_objects(col_name: str, data: InsertData):
    coll = db[col_name]
    if isinstance(data, list):
        await coll.insert_many(data)
    else:
        await coll.insert_one(data)

async def insert_player(data: InsertData):
    return await __insert_objects(PLAYERS, data)

async def insert_match(data: InsertData):
    return await __insert_objects(MATCHES, data)

async def insert_ranked_player(data: InsertData):
    return await __insert_objects(RANKED_PLAYERS, data)