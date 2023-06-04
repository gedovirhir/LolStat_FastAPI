from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient, ASCENDING

from src.config import config

from .enums import PLAYERS, MATCHES, RANKED_PLAYERS

MONGO_URL = f"mongodb://{config.mongo.MONGO_HOST}:{config.mongo.MONGO_PORT}"

mongo_db = MongoClient(MONGO_URL).get_database(config.mongo.MONGO_DB_NAME)

motor_client = AsyncIOMotorClient(MONGO_URL)

db = motor_client[config.mongo.MONGO_DB_NAME]
players = motor_client[PLAYERS]
matches = motor_client[MATCHES]
ranked_players = motor_client[RANKED_PLAYERS]
