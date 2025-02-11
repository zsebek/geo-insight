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