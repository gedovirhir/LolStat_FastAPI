from pydantic import BaseModel

from typing import List

class Participant(BaseModel):
    champion_name: str
    lane: str
    items: List[int]
    win: bool
    
    @classmethod
    def get_mongo_map(self):
        return {
            "champion_name": "$info.participants.championName",
            "lane": "$info.participants.lane",
            "items": [
                "$info.participants.item0",    
                "$info.participants.item1",    
                "$info.participants.item2",    
                "$info.participants.item3",    
                "$info.participants.item4",    
                "$info.participants.item5",    
                "$info.participants.item6",    
            ],
            "win": "$info.participants.win",
        }

"""class ItemRecInput(BaseModel):
    participants: List[Participant]"""
    