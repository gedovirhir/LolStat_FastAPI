from fastapi import APIRouter

from src.mongo.core import mongo_db

router = APIRouter(prefix="/lol")
