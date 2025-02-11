from typing import Dict, List
from models import Location

def update_country_metrics(country_code: str, round_score: int, round_distance: float, 
                           points_lost_per_country: Dict, distance_per_country: Dict, country_counts: Dict):
    """Updates metrics for a given country."""
    if country_code not in points_lost_per_country:
        points_lost_per_country[country_code] = 5000 - round_score
        distance_per_country[country_code] = round_distance
        country_counts[country_code] = 1
    else:
        points_lost_per_country[country_code] += 5000 - round_score
        distance_per_country[country_code] += round_distance
        country_counts[country_code] += 1

def calculate_average_metrics(points_lost_per_country: Dict, distance_per_country: Dict, country_counts: Dict):
    """Computes per-country average values."""
    return {
        "points_lost_per_country_average": {k: v / country_counts[k] for k, v in points_lost_per_country.items()},
        "distance_per_country_average": {k: v / country_counts[k] for k, v in distance_per_country.items()}
    }
