from sqlalchemy import BigInteger, Column, Integer, String
from TicTacToe.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger)
    user_name = Column(String)
    games_count = Column(Integer)
    lose_count = Column(Integer)
    wins_count = Column(Integer)
    lang = Column(String)