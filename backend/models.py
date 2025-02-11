from pydantic import BaseModel
from typing import List, Dict, Optional

class Location(BaseModel):
    lat: float
    lng: float
    country_code: str

class GuessedLocation(BaseModel):
    lat: float
    lng: float
    score: int

class GameStats(BaseModel):
    average_score: int
    average_distance: int
    average_time: int
    round_wise_points: List[int]
    round_wise_time: List[int]
    points_lost_per_country: Dict[str, int]
    distance_per_country: Dict[str, int]
    points_lost_per_country_average: Dict[str, float]
    distance_per_country_average: Dict[str, float]
    number_of_games: int
    number_of_rounds: int
    guessed_locations: List[GuessedLocation]
    round_locations: List[Location]
    countries: Dict[str, int]

class FullGameStats(BaseModel):
    moving: GameStats
    no_moving: GameStats
    nmpz: GameStats