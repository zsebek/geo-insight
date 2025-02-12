import json
from sqlalchemy.orm import Session
from requests import Session as reqSession
from models.gameplay import StandardGame, Duel, StandardGuess
from config.api_urls import BASE_URL_V3, BASE_URL_V4
from services.auth.session_manager import SessionManager
from database.geoguessr import get_db


def get_all_games():
    db = next(get_db())
    games = db.query(StandardGame).all()
    db.close()
    return [game.__dict__ for game in games]
    
def get_all_guesses():
    db: Session = next(get_db())
    guesses = db.query(StandardGuess).all()
    db.close()
    return [guess.__dict__ for guess in guesses]
    
def get_all_duels():
    db: Session = next(get_db())
    duels = db.query(Duel).all()
    db.close()
    return [duel.__dict__ for duel in duels]

def fetch_all():
    session = SessionManager.get_session()
    db = next(get_db())
    fetch_game_data(db, session)
    fetch_game_rounds(db, session)


def get_unprocessed_game_tokens(db: Session):
    """Returns a list of game tokens that do not yet have rounds stored."""
    existing_tokens = db.query(StandardGuess.game_token).distinct().all()
    existing_tokens = {token[0] for token in existing_tokens}  # Convert to set

    all_tokens = db.query(StandardGame.game_token).all()
    all_tokens = {token[0] for token in all_tokens}

    return list(all_tokens - existing_tokens)  # Tokens without rounds

def fetch_game_rounds(db: Session, session: reqSession):
    """Fetches round data for unprocessed games and stores them."""
    game_tokens = get_unprocessed_game_tokens(db)

    for token in game_tokens:
        try:
            response = session.get(f"{BASE_URL_V3}/games/{token}")
            if not response.ok:
                continue

            game = response.json()
            # add extra game metadata
            update_data = {}
            if "roundCount" in game:
                update_data[StandardGame.round_count] = game["roundCount"]
            if "timeLimit" in game:
                update_data[StandardGame.time_limit] = game["timeLimit"]
            if "state" in game:
                update_data[StandardGame.state] = game["state"]
            if update_data:
                db.query(StandardGame).filter(StandardGame.game_token == token).update(update_data)
            
            rounds = []
            for i, actual in enumerate(game["rounds"]):
                guess = game["player"]["guesses"][i]  # Matching guesses

                rounds.append(StandardGuess(
                    game_token=token,
                    round_number=i + 1,
                    actual_lat=actual["lat"],
                    actual_lng=actual["lng"],
                    actual_heading = actual['heading'],
                    actual_pitch=actual['pitch'],
                    actual_zoom=actual['zoom'],
                    actual_panoId=actual['panoId'],
                    country_code=actual.get("streakLocationCode", "UNKNOWN"),
                    guessed_lat=guess["lat"],
                    guessed_lng=guess["lng"],
                    score=int(guess["roundScore"]["amount"]),
                    distance_km=float(guess["distanceInMeters"]/1000),
                    time_spent_sec=int(guess["time"]),
                ))

            db.add_all(rounds)  # Bulk insert for efficiency
        except Exception as e:
            print(f"Error processing game {token}: {e}")
            continue  # Move to next game

    db.commit()



def fetch_game_data(db: Session, session: reqSession): 
    entries = (session.get(f"{BASE_URL_V4}/feed/private")).json()['entries']
    for entry in entries:
        games = json.loads(entry.get('payload'))
        if not games: continue
        
        if isinstance(games, dict):
            if 'gameMode' not in games:
                continue
            store_game(db, games)
        
        elif isinstance(games, list):
            for game in games:
                data = game['payload']
                store_game(db, data)

def store_game(db: Session, data: dict):
    """Parses GeoGuessr game data and stores it in the database."""
    is_standard = True
    if data['gameMode'] in ['BattleRoyaleDistance', 'Duels']:
        existing_game = db.query(Duel).filter(Duel.game_id == data["gameId"]).first()
        is_standard = False
    elif data['gameMode'] == 'Standard':
        existing_game = db.query(StandardGame).filter(StandardGame.game_token == data["gameToken"]).first()
    
    if existing_game:
        return
    
    new_game = StandardGame(
        map_slug=data["mapSlug"],
        map_name=data["mapName"],
        points=data["points"],
        game_token=data["gameToken"],
        game_mode=data["gameMode"],
    ) if is_standard else \
    Duel(
        game_id=data['gameId'],
        game_mode=data['gameMode'],
        competitive_game_mode=data['competitiveGameMode']
    )    
    db.add(new_game)  
    db.commit()

if __name__=="__main__":
    res = get_all_games()
    print(res)
    
