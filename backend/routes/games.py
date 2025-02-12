from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.geoguessr import get_db
from services.aggregation.geoguessr import store_game_data
router = APIRouter()

@router.post("/aggregate/{user_id}")
def aggregate_data(user_id: str, db: Session = Depends(get_db)):
    return store_game_data(db, user_id)