import requests
from requests import Session
import json
from config import BASE_URL_V3, BASE_URL_V4, GAME_SERVER_URL
import pandas as pd
from geopy.geocoders import Nominatim

def get_session(ncfa) -> Session:
    session = requests.Session()
    session.cookies.set("_ncfa", ncfa, domain="www.geoguessr.com")
    return session

def add_game_to_list(data: dict, games: list):
    """ return by value """
    is_standard = True
    if data['gameMode'] in ['BattleRoyaleDistance', 'Duels']:
        is_standard = False
    new_game = {
        "map_slug": data["mapSlug"],
        "map_name": data["mapName"],
        "points": data["points"],
        "game_token": data["gameToken"],
        "game_mode": data["gameMode"],
    } if is_standard else \
    {
        "game_id": data['gameId'],
        "game_mode": data['gameMode'],
        "competitive_game_mode": data['competitiveGameMode']
    }
    games.append(new_game)

def get_games(ncfa: str) -> list[dict]:
    """ returns games: list"""
    games = []
    session: Session = get_session(ncfa)
    entries = (session.get(f"{BASE_URL_V4}/feed/private")).json()['entries']
    for entry in entries:
        data = json.loads(entry['payload'])
        if not data:
            continue
        # handle a single game
        if isinstance(data, dict):
            if 'gameMode' not in data:  # looks for key 'gameMode' in dict, ignore badges
                continue
            add_game_to_list(data, games)
        # handle when data is a list of games
        elif isinstance(data, list):
            for game in data:
                payload = game['payload']
                if 'gameMode' not in payload:
                    continue
                add_game_to_list(payload, games)
    return games

def get_standard_guesses_from_tokens(tokens: list[str], ncfa: str) -> list[dict]:
    guesses = []
    session: Session = get_session(ncfa)
    for token in tokens:
        response = session.get(f"{BASE_URL_V3}/games/{token}")
        if not response.ok:
            continue
        game = response.json()
        for i, actual in enumerate(game["rounds"]):
            guess = game["player"]["guesses"][i]  # Matching guesses
            new_guess = \
                {
                "game_token": token,
                "round_number": i + 1,
                "actual_lat": actual["lat"],
                "actual_lng": actual["lng"],
                "actual_heading": actual['heading'],
                "actual_pitch": actual['pitch'],
                "actual_zoom": actual['zoom'],
                "actual_panoId": actual['panoId'],
                "country_code": actual.get("streakLocationCode", "UNKNOWN"),
                "guessed_lat": guess["lat"],
                "guessed_lng": guess["lng"],
                "score": int(guess["roundScore"]["amount"]),
                "distance_km": float(guess["distanceInMeters"]/1000),
                "time_spent_sec": int(guess["time"]),
                }
            guesses.append(new_guess)
    return guesses    

def print_game_details(tokens: list[str], ncfa: str):
    """Prints the full game details for each token."""
    session: Session = get_session(ncfa)
    for token in tokens:
        response = session.get(f"{BASE_URL_V3}/games/{token}")
        if not response.ok:
            print(f"Error getting game data for token: {token}")  # Print error if request fails
            continue

        try:
            game_data = response.json()
            print(json.dumps(game_data, indent=4)) # Print the full JSON response
            print("-" * 20)  # Separator between games
        except json.JSONDecodeError:
            print(f"Error decoding JSON for token: {token}") # Handle JSON decode errors
            print(response.text) # Optionally print the raw text of the response for debugging
            print("-" * 20)
        except Exception as e: # Catching other potential errors
            print(f"An unexpected error occurred: {e}")
            print("-" * 20)

def print_duel_details(tokens: list[str], ncfa: str):
    """Prints the full game details for each token."""
    session: Session = get_session(ncfa)
    for token in tokens:
        response = session.get(f"{GAME_SERVER_URL}/duels/{token}")
        if not response.ok:
            print(f"Error getting game data for token: {token}")  # Print error if request fails
            continue

        try:
            game_data = response.json()
            print(json.dumps(game_data, indent=4)) # Print the full JSON response
            print("-" * 20)  # Separator between games
        except json.JSONDecodeError:
            print(f"Error decoding JSON for token: {token}") # Handle JSON decode errors
            print(response.text) # Optionally print the raw text of the response for debugging
            print("-" * 20)
        except Exception as e: # Catching other potential errors
            print(f"An unexpected error occurred: {e}")
            print("-" * 20)

def get_games_guesses_duels_dataframes():
    ncfa: str = "CkEPxRnm%2BpatXNu92E7AgHIs9Cmyn5TqjGkLjgx15as%3DPmea5NC7KbJh2tv3vaWyo8uc4HQfJyHKyLyzSdep%2BtvkLTa2ak7d8%2F3XrIkvKzKK6B79dO9xH4IvVc6PTsCsf0rGV%2FswebIaTvb%2FeO6Qyz8%3D"
    games = get_games(ncfa)
    standard_games = [game for game in games if game['game_mode'] == 'Standard']
    standard_tokens = [game['game_token'] for game in standard_games]
    standard_guesses = get_standard_guesses_from_tokens(standard_tokens, ncfa)
    duels = [game for game in games if game not in standard_games]
    return pd.DataFrame(standard_games), pd.DataFrame(standard_guesses), pd.DataFrame(duels)

def geocode(guesses: pd.DataFrame):
    geolocator = Nominatim(user_agent="geoapp")
    length = len(guesses)
    progress = {"iter": 0}
    def reverse_geocode(row):
        print(f"{progress['iter']} / {length}")
        try:
            location = geolocator.reverse((row['guessed_lat'], row['guessed_lng']), exactly_one=True)
            progress['iter'] +=1
            return location.address if location else None
        except Exception as e:
            return f"Error: {e}"

    # Apply reverse geocoding to each row
    guesses['location'] = guesses.apply(reverse_geocode, axis=1)
    return guesses

if __name__=="__main__":
    # define token for debugging; call main function.
    ncfa: str = "CkEPxRnm%2BpatXNu92E7AgHIs9Cmyn5TqjGkLjgx15as%3DPmea5NC7KbJh2tv3vaWyo8uc4HQfJyHKyLyzSdep%2BtvkLTa2ak7d8%2F3XrIkvKzKK6B79dO9xH4IvVc6PTsCsf0rGV%2FswebIaTvb%2FeO6Qyz8%3D"
    ncfa_gameserver: str = "Y2iRgBhFdKt7TOhYsSzbK7NuJm204qTC2yJ6APJvV00%3DPmea5NC7KbJh2tv3vaWyo8uc4HQfJyHKyLyzSdep%2BtvkLTa2ak7d8%2F3XrIkvKzKK6B79dO9xH4IvVc6PTsCsf%2Fo%2B4S%2BXBIJRukGooMGHkfE%3D"
    
    standard_games, guesses, duels = get_games_guesses_duels_dataframes()

    # Print the DataFrames
    # print("Standard Games DataFrame:")
    # print(standard_games)

    # print("\nGuesses DataFrame:")
    # print(guesses)

    # print("\nDuels DataFrame:")
    print(duels)

    #Geocode and print the updated guess dataframe
    #guesses = geocode(guesses)
    #print("\nGuesses DataFrame with Geocoding:")
    #print(guesses)

    # Save the geocoded guesses DataFrame to a CSV file
    #guesses.to_csv("geocoded_guesses.csv", index=False, encoding='utf-8')  # Most common format
    #print("\nGeocoded guesses saved to geocoded_guesses.csv")

    # Test print_game_details
    # First token is Standard game [works], second and third are duels [don't work]
    # Need to figure out how to print Duel & BattleRoyale info. perhaps a different game endpoint or something. Since the tokens below (different format than 1-player) don't work
    example_tokens = ["Xv6TIlyL73VMvSGT", "5f5b948b-a397-43c1-9ca0-8671bf078fd6", "8ef1d8b7-e584-4bab-b257-f7d7f871208c"] # *REPLACE with your actual tokens*
    print_game_details(example_tokens, ncfa)
    print_duel_details(example_tokens, ncfa_gameserver)