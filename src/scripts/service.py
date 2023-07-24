import json
import asyncio
import aiofiles
from pymongo.errors import DuplicateKeyError

from src.riotapi.enums import TIER_ENUM, DIVISION_ENUM

from src.riotapi.core import lwatcher

from src.mongo.service import insert_ranked_player, insert_match
from src.mongo.service import RiotMongo
from src.lol_service.service import get_player

from .enums import MAX_PAGE_LEAGUE_ENTRIES

async def download_league_entries(tier, div):
    for p in range(1, MAX_PAGE_LEAGUE_ENTRIES, 1):
        try:
            entries = lwatcher.league.entries(
                region='ru', 
                queue="RANKED_SOLO_5x5",
                tier=tier,
                division=div,
                page=p
            )
        except Exception as ex:
            await asyncio.sleep(130)

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

def download_player_matches(player_name: str):
    p = lwatcher.summoner.by_name('ru', player_name)
    puuid = p['puuid']
    match_list = lwatcher.match.matchlist_by_puuid(region='ru', puuid=puuid, count=100)
    
    return match_list

async def download_matches(matches_ids: list):
    for id_ in matches_ids:
        errors = 0
        while True:
            try:
                match_ = lwatcher.match.by_id('ru', id_)
                await insert_match(match_)
                break
            except DuplicateKeyError:
                print('DublicateKey')
                continue
            except Exception as e:
                print(e)
                errors += 1
                if errors > 3:
                    await asyncio.sleep(130)
                    errors = 0
                else:
                    await asyncio.sleep(10)

async def delete_duplicates(match_ids:list):
    res = []
    
    for id_ in match_ids:
        v = await RiotMongo.match.get_match(id_)
        if not v:
            res.append(id_)
    
    return res

async def download_diamond_matches():
    #await download_league_entries(tier='DIAMOND', div='I')
    for i in range(3, MAX_PAGE_LEAGUE_ENTRIES, 1):
        entries = await RiotMongo.league.get_entries(page=i)
        
        for e in entries:
            p = await get_player(summonerId=e.summonerId)
            matches = lwatcher.match.matchlist_by_puuid(region='ru', puuid=p.puuid, count=20)
            matches = await delete_duplicates(matches)
            await download_matches(matches)
    
            
    
        