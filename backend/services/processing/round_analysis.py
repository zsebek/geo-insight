from typing import List, Dict
from models import GuessedLocation

def process_rounds(game_rounds: List[Dict], player_guesses: List[Dict]) -> Dict:
    """Processes per-round data for score, time, and guessed locations."""
    round_wise_points = []
    round_wise_time = []
    guessed_locations = []

    for actual, guess in zip(game_rounds, player_guesses):
        round_wise_points.append(guess['roundScore']['amount'])
        round_wise_time.append(guess['time'])
        guessed_locations.append(GuessedLocation(lat=guess['lat'], lng=guess['lng'], score=guess['roundScore']['amount']))
    
    return {
        "round_wise_points": round_wise_points,
        "round_wise_time": round_wise_time,
        "guessed_locations": guessed_locations
    }
