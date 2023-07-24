from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select

from typing import List

from src.mongo.service import RiotMongo
from src.riotapi.service import RiotAPI

from src.database import AutocommitSession, DbSession
from src.auth.service.dependencies import current_user, verify_token

from .models import PostProfile, UserLolProfile, ResponseProfile
from ..service import get_player, get_player_entries

router = APIRouter(prefix='/profile', dependencies=[Depends(verify_token)])

@router.post('/')
async def post_profile(profile: PostProfile, db: DbSession, user: current_user): 
    try:
        player = await get_player(
            name=profile.name
        )
        if not player:
            raise
    except:
        raise HTTPException(
            404,
            "No profile with that region and name"
        )
        
    new_user_profile = UserLolProfile(
        user_id=user.user_id,
        puuid=player.puuid
    )
    try:
        db.add(new_user_profile)
        await db.commit()
    except Exception as e:
        raise HTTPException(
            400,
            "You already added this profile"
        )

@router.get('/me', response_model=List[ResponseProfile])
async def get_lol_profile(user: current_user, db: DbSession):
    profiles_puuids = await db.execute(
        select(UserLolProfile.puuid).where(UserLolProfile.user==user)
    )
    profiles = []
    for puuid in profiles_puuids.scalars():
        lol_player = await get_player(
            puuid=puuid
        )
        entries = await get_player_entries(
            lol_player.summonerId
        )

        profiles.append(
            {
                **lol_player.dict(),
                'league_entries': entries
            }
        )
        
    return profiles
    