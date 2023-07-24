from typing import List

from src.mongo.service import RiotMongo
from src.riotapi.service import RiotAPI

from src.riotapi.models import PlayerBaseInfo, QueuePlayerStat


async def get_player(**identity_field) -> PlayerBaseInfo:
    player = await RiotMongo.player.get_by_identity_field(
        **identity_field
    )
    
    if not player:  
        player = await RiotAPI.player.get_by_identity_field(
            **identity_field
        )
        await RiotMongo.player.insert_player(player)
    
    return player

async def get_player_entries(summoner_id: str) -> List[QueuePlayerStat]:
    entries = await RiotAPI.player.get_league_entries(
        summoner_id
    )
    
    return entries