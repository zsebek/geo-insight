


# from typing import List, Dict
# from models.stats import GameStats

# def compute_game_stats(game_data: List[Dict]) -> GameStats:
#     """Compute aggregated game statistics from raw game data."""
#     total_score = sum(game['player']['totalScore']['amount'] for game in game_data)
#     total_distance = sum(game['player']['totalDistance'] for game in game_data)
#     total_time = sum(game['player']['totalTime'] for game in game_data)

#     return GameStats(
#         average_score=int(total_score / len(game_data)) if game_data else 0,
#         average_distance=int(total_distance / len(game_data)) if game_data else 0,
#         average_time=int(total_time / len(game_data)) if game_data else 0,
#         round_wise_points=[],
#         round_wise_time=[],
#         points_lost_per_country={},
#         distance_per_country={},
#         points_lost_per_country_average={},
#         distance_per_country_average={},
#         number_of_games=len(game_data),
#         number_of_rounds=0,
#         guessed_locations=[],
#         round_locations=[],
#         countries={}
#     )
