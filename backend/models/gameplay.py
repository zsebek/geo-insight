from sqlalchemy import Column, Integer, String
from database.geoguessr import Base

class StandardGame(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    map_slug = Column(String, index=True)  # text in pgAdmin
    map_name = Column(String)
    points = Column(Integer)
    game_token = Column(String, unique=True, index=True)
    game_mode = Column(String)


class Duel(Base):
    __tablename__ = "duels"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    game_id = Column(String, index=True)
    game_mode = Column(String)
    competitive_game_mode = Column(String)
