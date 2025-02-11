from services.processing.game_stats import compute_game_stats
from services.processing.country_metrics import update_country_metrics, calculate_average_metrics
from services.processing.round_analysis import process_rounds
from backend.services.auth.login import get_game_tokens

def calculate_game_stats(ncfa, num_games):
    """Master function that delegates to smaller processing modules."""
    # Fetch game data
    game_data = get_game_tokens(ncfa, num_games)

    # Compute core stats
    stats = compute_game_stats(game_data)

    # Process round details
    round_data = process_rounds(game_data['rounds'], game_data['player']['guesses'])
    stats.round_wise_points = round_data["round_wise_points"]
    stats.round_wise_time = round_data["round_wise_time"]
    stats.guessed_locations = round_data["guessed_locations"]

    # Compute country metrics
    country_metrics = calculate_average_metrics(stats.points_lost_per_country, stats.distance_per_country, stats.countries)
    stats.points_lost_per_country_average = country_metrics["points_lost_per_country_average"]
    stats.distance_per_country_average = country_metrics["distance_per_country_average"]

    return stats
