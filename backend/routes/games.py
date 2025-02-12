from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.aggregation.geoguessr import fetch_all
router = APIRouter()

@router.get("/fetch-all")
def aggregate_data():
    return fetch_all()
