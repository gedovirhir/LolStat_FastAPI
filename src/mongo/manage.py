from pymongo import ASCENDING

from .core import mongo_db
from .enums import MATCHES, RANKED_PLAYERS

def initialize_db():
    # Creating unique index
    mongo_db[MATCHES].create_index([("metadata.matchId", ASCENDING)], unique=True)
    mongo_db[RANKED_PLAYERS].create_index([('summonerId', ASCENDING)], unique=True)
    