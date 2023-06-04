import json
import asyncio
import aiofiles
from pymongo.errors import DuplicateKeyError

from src.riotapi.enums import TIER, DIVISION
from src.riotapi.service import get_league_entries_players, get_player_by_name

from src.mongo.service import insert_ranked_player

from .enums import MAX_PAGE_LEAGUE_ENTRIES

async def download_league_entries():
    for t in TIER:
        for d in DIVISION:
            for p in range(1, MAX_PAGE_LEAGUE_ENTRIES, 1):
                try:
                    entries = get_league_entries_players(
                        region='ru', 
                        tier=t,
                        division=d,
                        page=p
                    )
                except Exception as ex:
                    await asyncio.sleep(120)

                for e in entries:
                    await insert_ranked_player(e)
       
async def check_():
    async def get_p():
        for _ in range(10):
            player = await asyncio.to_thread(get_player_by_name, 'ru', 'gedovirhir')
            async with aiofiles.open('players_check.json', 'a') as f:
                await f.write(f"{player}\n".replace("'", '"'))
    
    tasks = [get_p() for _ in range(10)]
    await asyncio.gather(*tasks)