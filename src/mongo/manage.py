from pymongo import ASCENDING

from .core import mongo_db
from .enums import MATCHES, LEAGUE_ENTRIES

def initialize_db():
    # Creating unique index
    mongo_db[MATCHES].create_index([("metadata.matchId", ASCENDING)], unique=True)
    
    
    mongo_db[LEAGUE_ENTRIES].create_index([('summonerId', ASCENDING)], unique=True)
    