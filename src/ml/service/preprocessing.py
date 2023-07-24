import pandas as pd
import json
from pydantic import parse_obj_as
from fastapi.encoders import jsonable_encoder

from typing import List

from src.mongo.service import RiotMongo

from ..core import encoder
from ..models import Participant

ItemRecInput = List[Participant]

async def download_mongo_participants() -> ItemRecInput:
    aggr = [
        {
            "$unwind": "$info.participants"
        },
        {
        "$project": Participant.get_mongo_map()
        },
    ]
    
    partc = await RiotMongo.match.get_aggregation(aggr)
    
    data = parse_obj_as(ItemRecInput, partc)
    
    return data

async def preprocess_participants(data: ItemRecInput = None):
    data = await download_mongo_participants()
    data_json = jsonable_encoder(data)
    
    data_f = pd.read_json(json.dumps(data_json))
    
    data_f['champion_name'] = encoder().fit_transform(data_f['champion_name'])
    data_f['lane'] = encoder().fit_transform(data_f['lane'])

    item_encoder = encoder()
    unique_item_ids = sorted(list(set(x for item_list in data_f['items'] for x in item_list)))
    item_encoder.fit(unique_item_ids)
    data_f['items'] = data_f['items'].apply(
        lambda x: item_encoder.transform(x).tolist()
    )  
    
    
    