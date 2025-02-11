from fastapi import APIRouter, Depends
from services.processing import calculate_game_stats

router = APIRouter()

@router.get("/calculate")
def get_statistics(ncfa: str, num_games: int = 50):
    """Processes and returns statistics for a given number of games."""
    return calculate_game_stats(ncfa, num_games)
