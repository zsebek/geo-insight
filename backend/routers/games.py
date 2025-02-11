from fastapi import APIRouter
from services.aggregation.get_games import get_game_tokens

router = APIRouter()

@router.get("/tokens")
def fetch_game_tokens(ncfa: str):
    """Fetches recent game tokens."""
    return get_game_tokens(ncfa)
