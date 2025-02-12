from fastapi import APIRouter
from services.aggregation.geoguessr import fetch_all, get_all_duels, get_all_games, get_all_guesses
router = APIRouter()

@router.get("/fetch-all")
def aggregate_data():
    return fetch_all()

@router.get("/games/get/all")
def all_games():
    print("✅ Fetching all games from the database...")
    games = get_all_games() 
    print(f"got {games}")
    return games

@router.get("guesses/get/all")
def all_guesses():
    return get_all_guesses()

@router.get("duels/get/all")
def all_duels():
    return get_all_duels()