import asyncio
import json
from uuid import uuid4
import random

from fastapi import APIRouter, Depends , HTTPException
from fastapi.responses import JSONResponse, Response

from typing import Coroutine, Dict

from src.auth.service.dependencies import verify_token
from src.auth.service.crypt import hash_password
from src.mongo.service import RiotMongo
from src.redis.core import RedisSession

from .models import MatchReportRequestSchema, MatchReportsResponse, ItemRecRequest
from .core import request_sessions
from .enums import ITEMS

router = APIRouter(prefix='/statistic', dependencies=[Depends(verify_token)])

@router.post('/match_report')
async def post_matches_report_request(request: MatchReportRequestSchema):
    try:
        request_id = str(uuid4())
        request_sessions.update({request_id: None})
        
        mongo_stages = request.to_mongo_script()
        task = RiotMongo.match.get_aggregation(mongo_stages)

        await asyncio.create_task(delayed_task(request_id, task))
        
        return JSONResponse(
            content={"request_id": request_id},
            status_code=201
        )
    except Exception as ex:
        raise HTTPException(
            400
        )

async def delayed_task(session_id: str, task: Coroutine):
    res = await task
    request_sessions[session_id] = res

@router.get('/match_report/{request_id}', response_model=MatchReportsResponse)
async def get_match_report(request_id: str):
    if request_id not in request_sessions:
        raise HTTPException(404, "Not found")
    
    res = request_sessions.get(request_id)
    
    if res:
        del request_sessions[request_id]
        resp = MatchReportsResponse(
            info=res,
            request_id=request_id
        )
        return resp
    
    else:
        return Response(status_code=202)


"""with open('kekekekes.json', 'w') as f:
        json.dump(mongo_stages, f, indent=4"""        

@router.post('/item_rec', response_model=Dict[str, int])
async def get_item_rec(items_request: ItemRecRequest, redis: RedisSession):
    to_hash = f"""
    /iterm_rec {items_request.dict()}
    """
    hash_ = hash(to_hash)
    v = redis.get(hash_)
    
    if not v: 
        v = random.choice(ITEMS)
    
        redis.set(hash_, v)
    
    return JSONResponse(
        {
            "item_id": v
        }
    )
