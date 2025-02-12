from sqlalchemy import Column, Integer, String, Float
from database.geoguessr import Base

class StandardGame(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    map_slug = Column(String, index=True)  # text in pgAdmin
    map_name = Column(String)
    points = Column(Integer)
    game_token = Column(String, unique=True, index=True)
    game_mode = Column(String)
    round_count = Column(Integer)
    time_limit = Column(Float)
    state = Column(String)

class StandardGuess(Base):
    __tablename__ = "guesses"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    game_token = Column(String, index=True)  # Foreign Key to StandardGame
    round_number = Column(Integer)  # The round index (1 to 5 in GeoGuessr)
    actual_lat = Column(Float)
    actual_lng = Column(Float)
    actual_heading = Column(Float)
    actual_pitch = Column(Float)
    actual_zoom = Column(Float)
    actual_panoId = Column(String)
    country_code = Column(String)  # Country where the round took place
    guessed_lat = Column(Float)
    guessed_lng = Column(Float)
    score = Column(Integer)
    distance_km = Column(Float)
    time_spent_sec = Column(Float)
    # timed_out
    

    


class Duel(Base):
    __tablename__ = "duels"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    game_id = Column(String, index=True)
    game_mode = Column(String)
    competitive_game_mode = Column(String)
