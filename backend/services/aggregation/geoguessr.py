import json
from sqlalchemy.orm import Session
from models.gameplay import StandardGame, Duel
from config.api_urls import BASE_URL_V4
from services.auth.session_manager import SessionManager
from database.geoguessr import get_db

def fetch_game_data():
    session = SessionManager.get_session()
    db = next(get_db())
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
    fetch_game_data()
    
