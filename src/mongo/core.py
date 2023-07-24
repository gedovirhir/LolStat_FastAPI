from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient, ASCENDING
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.cursor import Cursor

from src.config import config

from .enums import PLAYERS, MATCHES, LEAGUE_ENTRIES

MONGO_URL = f"mongodb://{config.mongo.MONGO_HOST}:{config.mongo.MONGO_PORT}"

mongo_db = MongoClient(MONGO_URL).get_database(config.mongo.MONGO_DB_NAME)

motor_client = AsyncIOMotorClient(MONGO_URL)

motor_db: MongoClient = motor_client[config.mongo.MONGO_DB_NAME]
players = motor_client[PLAYERS]
matches = motor_client[MATCHES]
LEAGUE_ENTRIES = motor_client[LEAGUE_ENTRIES]
