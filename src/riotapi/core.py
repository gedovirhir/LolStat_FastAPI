from riotwatcher import LolWatcher

from src.config import config

lwatcher = LolWatcher(
    api_key=config.riot.RIOT_API_KEY
)
