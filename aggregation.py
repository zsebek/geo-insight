import requests
import time
from requests import Session
import json
from config import BASE_URL_V3, BASE_URL_V4, GAME_SERVER_DOMAIN, GAME_SERVER_URL
import pandas as pd
from geopy.geocoders import Nominatim
from datetime import datetime

def get_session(ncfa: str, domain: str = "www.geoguessr.com", session_user: dict[str, str] = None) -> Session:
    session = requests.Session()
    session.cookies.set("_ncfa", ncfa, domain=domain)
    
    # supply optional session_user cookie when domain is https://game-server.geoguessr.com
    if session_user:
        """
            got game-server request to work with, let's see if hjSessionUser_id changes for you
            cookies = {
                "_ncfa": "l920 ... blah",
                "_hjSessionUser_2662791": "eyJp ... blah",
            }
        """
        for key, val in session_user.items():
            session.cookies.set(key, val, domain=domain)
    
    return session

def add_game_to_list(data: dict, games: list):
    """ return by value """
    is_standard_game = True
    is_standard_duel = False
    is_nonstandard_duel = False
    is_challenge = False
    
    if data['gameMode'] in ['Streak', 'LiveChallenge', 'Bullseye', 'CompetitiveCityStreak']:
        return
    
    if data['gameMode'] in ['BattleRoyaleDistance', 'Duels', 'TeamDuels', 'BattleRoyaleCountries']:
        is_standard_duel = True
        is_standard_game = False
        if not data.get('competitiveGameMode', False):
            is_nonstandard_duel = True
            is_standard_duel = False
    if data.get('challengeToken', False):
        is_challenge = True
        is_standard_game = False

    new_game = {
        "map_slug": data["mapSlug"],
        "map_name": data["mapName"],
        "points": data["points"],
        "game_token": data["gameToken"],
        "game_mode": data["gameMode"],
    } if is_standard_game else \
    {
        "game_id": data['gameId'],
        "game_mode": data['gameMode'],
        "competitive_game_mode": data['competitiveGameMode']
    } if is_standard_duel else \
    {
        "game_id": data['gameId'],
        "game_mode": data['gameMode'],
        "party_id": data['partyId'],
    } if is_nonstandard_duel else \
    {
        "map_slug": data["mapSlug"],
        "map_name": data["mapName"],
        "points": data["points"],
        "game_token": data["challengeToken"],
        "game_mode": data["gameMode"],
        "is_daily": data["isDailyChallenge"]
    } if is_challenge else \
    {
        
    }
    # TODO: support Challenges model
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

def get_duel_guesses_from_tokens(tokens: list[str], ncfa: str, session_user: dict[str, str]) -> list[dict]:
    guesses = []
    session: Session = get_session(ncfa, GAME_SERVER_DOMAIN, session_user)
    for token in tokens:
        response = session.get(f"{GAME_SERVER_URL}/duels/{token}")
        if not response.ok:
            print(f"Error getting duel data for token: {token}")
            continue
        try:
            game_data = response.json()
            for team in game_data["teams"]:
                for player in team["players"]:
                    for guess in player["guesses"]:
                        round_data = next((r for r in game_data["rounds"] if r["roundNumber"] == guess["roundNumber"]), None)
                        round_results_data = next((rr for rr in team["roundResults"] if rr["roundNumber"] == guess["roundNumber"]), None)  # Get round results
                        if round_data and round_results_data:  # Both must exist
                            new_guess = {
                                "game_token": game_data["gameId"],
                                "round_number": guess["roundNumber"],
                                "actual_lat": round_data["panorama"]["lat"],
                                "actual_lng": round_data["panorama"]["lng"],
                                "actual_heading": round_data["panorama"]['heading'],
                                "actual_pitch": round_data["panorama"]['pitch'],
                                "actual_zoom": round_data["panorama"]['zoom'],
                                "actual_panoId": round_data["panorama"]['panoId'],
                                "country_code": round_data["panorama"].get("countryCode", "UNKNOWN"),
                                "guessed_lat": guess["lat"],
                                "guessed_lng": guess["lng"],
                                "score": int(guess["score"]),
                                "distance_km": float(guess["distance"] / 1000),
                                "time_spent_sec": (
                                    (
                                        datetime.fromisoformat(guess["created"].replace("Z", "+00:00")) - 
                                        datetime.fromisoformat(round_data["startTime"].replace("Z", "+00:00"))
                                    ).total_seconds() if round_data.get("startTime") else None
                                ),
                                "player_id": player["playerId"],
                                "team_name": team["name"],
                                "health_before": round_results_data.get("healthBefore"), 
                                "health_after": round_results_data.get("healthAfter"),  
                                "multiplier": round_data.get("multiplier"),  
                                "damage_multiplier": round_data.get("damageMultiplier")  
                            }
                            guesses.append(new_guess)
        except json.JSONDecodeError:
            print(f"Error decoding JSON for token: {token}")
            print(response.text)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
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

def print_duel_details(tokens: list[str], ncfa: str, session_user: dict[str, str]):
    """Prints the full game details for each token."""
    session: Session = get_session(ncfa, GAME_SERVER_DOMAIN, session_user)
    for token in tokens:
        
        response = session.get(f"{GAME_SERVER_URL}/duels/{token}")
        if not response.ok:
            print(f"Error getting duel data for token: {token}")  # Print error if request fails
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
    ncfa_gameserver: str = "I9208e6tk3iIHYUfPiXhU2c3d9HYqsNhqlPXjOlc700%3DPmea5NC7KbJh2tv3vaWyo8uc4HQfJyHKyLyzSdep%2BtvkLTa2ak7d8%2F3XrIkvKzKK6B79dO9xH4IvVc6PTsCsfzkj5ZFpNoUAPMbHFo5OjOc%3D"
    session_user = {
         "_hjSessionUser_2662791": "eyJpZCI6ImY2YzRhYjlkLTdmNDAtNTlhYy05MjA1LTRmMDZkOTM5ZjhlNSIsImNyZWF0ZWQiOjE3MjgwODM1MDAxMzYsImV4aXN0aW5nIjp0cnVlfQ=="
    }
    games = get_games(ncfa)
    standard_games = [game for game in games if game['game_mode'] == 'Standard']
    standard_tokens = [game['game_token'] for game in standard_games]
    standard_guesses = get_standard_guesses_from_tokens(standard_tokens, ncfa)
    duel_games = [game for game in games if game['game_mode'] == 'Duels']
    duel_tokens = [game['game_id'] for game in duel_games]
    duel_guesses = get_duel_guesses_from_tokens(duel_tokens, ncfa_gameserver, session_user)
    return pd.DataFrame(standard_games), pd.DataFrame(standard_guesses), pd.DataFrame(duel_games), pd.DataFrame(duel_tokens), pd.DataFrame(duel_guesses)

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


def get_all_games(ncfa: str) -> list[dict]:
    """Fetch all game entries from the GeoGuessr API using pagination tokens."""
    session = get_session(ncfa)  # Your function for session auth
    all_games = []
    pagination_token = None  # Start without a token

    while True:
        params = {}
        if pagination_token:
            params["paginationToken"] = pagination_token  # Use token if available

        # response = session.get(f"{BASE_URL_V4}/feed/friends", params=params)
        response = session.get(f"{BASE_URL_V4}/feed/private", params=params)

        if response.status_code == 429:
            print("Rate limited. Sleeping for 10 seconds...")
            time.sleep(10)
            continue
        elif response.status_code != 200:
            print(f"Request failed: {response.text}")
            break

        try:
            data = response.json()
            entries = data.get('entries', [])
            pagination_token = data.get("paginationToken")  # Extract new token

            if not entries:
                break
            if not pagination_token:
                print("No pagination token found. Stopping.")
                break
            for entry in entries:
                data = json.loads(entry['payload'])
                if not data:
                    continue
                # handle a single game
                if isinstance(data, dict):
                    if 'gameMode' not in data:  # looks for key 'gameMode' in dict, ignore badges
                        continue
                    add_game_to_list(data, all_games)
                # handle when data is a list of games
                elif isinstance(data, list):
                    for game in data:
                        payload = game['payload']
                        if 'gameMode' not in payload:
                            continue
                        add_game_to_list(payload, all_games)

        except requests.exceptions.JSONDecodeError:
            print("Invalid JSON response. Stopping.")
            break

    return pd.DataFrame(all_games)
    

if __name__=="__main__":
    ncfa = "OSNSzcFekc1dEHNEHcHJqBT%2FD9Y7xS1lgmEHUpPYm3s%3DPmea5NC7KbJh2tv3vaWyo8uc4HQfJyHKyLyzSdep%2BtvkLTa2ak7d8%2F3XrIkvKzKK6B79dO9xH4IvVc6PTsCsfwnkjySGP9%2FXgFwPD3nN40Q%3D"
    
    all_games = get_all_games(ncfa)
    print("\nAll games dataframe")
    print(all_games)
    # define tokens for debugging; call main function.
    ncfa: str = "CkEPxRnm%2BpatXNu92E7AgHIs9Cmyn5TqjGkLjgx15as%3DPmea5NC7KbJh2tv3vaWyo8uc4HQfJyHKyLyzSdep%2BtvkLTa2ak7d8%2F3XrIkvKzKK6B79dO9xH4IvVc6PTsCsf0rGV%2FswebIaTvb%2FeO6Qyz8%3D"
    ncfa_gameserver: str = "I9208e6tk3iIHYUfPiXhU2c3d9HYqsNhqlPXjOlc700%3DPmea5NC7KbJh2tv3vaWyo8uc4HQfJyHKyLyzSdep%2BtvkLTa2ak7d8%2F3XrIkvKzKK6B79dO9xH4IvVc6PTsCsfzkj5ZFpNoUAPMbHFo5OjOc%3D"
    session_user = {
         "_hjSessionUser_2662791": "eyJpZCI6ImY2YzRhYjlkLTdmNDAtNTlhYy05MjA1LTRmMDZkOTM5ZjhlNSIsImNyZWF0ZWQiOjE3MjgwODM1MDAxMzYsImV4aXN0aW5nIjp0cnVlfQ=="
    }
    # Call primary Data gathering function
    standard_games, standard_guesses, duel_games, duel_tokens, duel_guesses = get_games_guesses_duels_dataframes()

    # Print the DataFrames
    # print("Standard Games DataFrame:")
    # print(standard_games)

    # print("\nGuesses DataFrame:")
    # print(guesses)

    print("\nduel_games DataFrame:")
    print(duel_games)

    # print("\nduel_tokens DataFrame:")
    # print(duel_tokens)

    print("\nduel_guesses DataFrame:")
    print(duel_guesses)

    #Geocode and print the updated guess dataframe
    duel_guesses = geocode(duel_guesses)
    print("\nDuel_Guesses DataFrame with Geocoding:")
    print(duel_guesses)

    # Save the geocoded guesses DataFrame to a CSV file
    duel_guesses.to_csv("geocoded_guesses_duels.csv", index=False, encoding='utf-8')  # Most common format
    print("\nGeocoded guesses saved to geocoded_guesses_duels.csv")

    
    all_games = get_all_games(ncfa)
    print("\nAll games dataframe")
    #### Debugging Additional example Tokens; Testing Duel Helper Functions and Duel Guesses Function

    # Test print_game_details
    # First token is Standard game [works], second and third are duels [don't work]
    # Need to figure out how to print Duel & BattleRoyale info. perhaps a different game endpoint or something. Since the tokens below (different format than 1-player) don't work
    # example_tokens = ["8ef1d8b7-e584-4bab-b257-f7d7f871208c"] 
    # print_game_details(example_tokens, ncfa)
    # print_duel_details(example_tokens, ncfa_gameserver, session_user)

    # duel_data = get_duel_guesses_from_tokens(example_tokens, ncfa_gameserver, session_user)

    # if duel_data: 
    #     print(json.dumps(duel_data, indent=4))

