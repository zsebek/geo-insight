from fastapi import APIRouter
from services.processing.game_stats import compute_game_stats

router = APIRouter()

@router.get("/calculate")
def get_statistics(ncfa: str, num_games: int = 50):
    """Processes and returns statistics for a given number of games."""
    return compute_game_stats(ncfa, num_games)
