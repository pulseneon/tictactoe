import datetime
import os
from dotenv import load_dotenv
from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer, String, create_engine, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker
from env import DB_USER, DB_NAME, DB_HOST, DB_PASS


class Base(DeclarativeBase): pass

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    games_count = Column(Integer)
    lose_count = Column(Integer)
    wins_count = Column(Integer)
    rating = Column(Integer, default=100) # at least zero initially 100 and give 5 for win
    lang = Column(String)
    game_id = Column(Integer) # if None => user in menu

class Game(Base):
    __tablename__ = "game"
    id = Column(Integer, primary_key=True, index=True)
    gamefield_id = Column(Integer, ForeignKey("gamefield.id"), nullable=False)
    first_player_id = Column(BigInteger, nullable=False) # изначально крестики
    second_player_id = Column(BigInteger, nullable=False) # изначально нолики
    move_player = Column(Boolean, nullable=False, default=True) 
    created_on = Column(DateTime(timezone=True), default=func.now())

class Gamefield(Base):
    __tablename__ = "gamefield"
    game = relationship("Game") # 0 - пусто, 1 - крестик, 2 - нолик
    id = Column(Integer, primary_key=True, index=True)
    field1 = Column(Integer, nullable=False, default=0)
    field2 = Column(Integer, nullable=False, default=0)
    field3 = Column(Integer, nullable=False, default=0) 
    field4 = Column(Integer, nullable=False, default=0)
    field5 = Column(Integer, nullable=False, default=0)
    field6 = Column(Integer, nullable=False, default=0)
    field7 = Column(Integer, nullable=False, default=0)
    field8 = Column(Integer, nullable=False, default=0)
    field9 = Column(Integer, nullable=False, default=0)

class Database:
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
    Base.metadata.create_all(bind=engine)   

    def clear_database(self):
        Base.metadata.drop_all(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)  
    
    def register_user(self, message, selected_lang):
        Session = sessionmaker(autoflush=False, bind=self.engine)
        if self.find_user(message.from_user.id) is not None:
            return False
        with Session(autoflush=False, bind=self.engine) as db:
            new_user = User(
                user_id = message.from_user.id,
                username = message.from_user.username,
                first_name = message.from_user.first_name,
                last_name = message.from_user.last_name,
                games_count = 0,
                lose_count = 0,
                wins_count = 0,
                lang = selected_lang
            )
            
            db.add(new_user)
            db.commit()
        return True
    
    def find_user(self, user_id) -> object:
        Session = sessionmaker(autoflush=False, bind=self.engine)
        with Session(autoflush=False, bind=self.engine) as db:
            user = db.query(User).filter(User.user_id == user_id).first()
            db.close()
            if user is not None:
                return user
            
        return None
    
    def create_game(self, user_id_1, user_id_2) -> object:
        if self.find_user(user_id_1).game_id is not None or \
            self.find_user(user_id_2).game_id is not None:
            return False
        
        if user_id_1 == user_id_2:
            return False

        Session = sessionmaker(autoflush=False, bind=self.engine)
        with Session(autoflush=False, bind=self.engine) as db:
            new_gamefield = Gamefield()
            db.add(new_gamefield)
            db.commit()

            new_game = Game(
                gamefield_id = new_gamefield.id,
                first_player_id = user_id_1,
                second_player_id = user_id_2
            )

            db.add(new_game)

            # refresh users game_id
            user_one = self.find_user(user_id_1)
            user_two = self.find_user(user_id_2)
            user_one.game_id = new_game.id
            user_two.game_id = new_game.id
            db.delete(user_one)
            db.delete(user_two)
            db.add(user_one)
            db.add(user_two)

            db.commit()
            db.close()

        return new_game

    def find_game(self, game_id) -> object:
        Session = sessionmaker(autoflush=False, bind=self.engine)
        with Session(autoflush=False, bind=self.engine) as db:
            game = db.query(Game).filter(Game.id == game_id).first()
            db.close()
            if game is not None:
                return game
        return None
    
    def find_gamefield(self, gamefield_id) -> object:
        Session = sessionmaker(autoflush=False, bind=self.engine)
        with Session(autoflush=False, bind=self.engine) as db:
            gamefield = db.query(Gamefield).filter(Gamefield.id == gamefield_id).first()
            db.close()
            if gamefield is not None:
                return gamefield
        return None

    # в теории работает
    def finish_game(self, first_player, second_player, winner): 
        '''
          winner = 0 - draw
          winner = 1 - first_player win, 
          winner = 2 - second_player win
        '''

        Session = sessionmaker(autoflush=False, bind=self.engine)
        with Session(autoflush=False, bind=self.engine) as db:
            user_one = self.find_user(first_player)
            user_two = self.find_user(second_player)
            
            db.delete(user_one)
            db.delete(user_two)
            
            user_one.game_id = None
            user_two.game_id = None
            
            user_one.games_count += 1
            user_two.games_count += 1

            if winner == 1:
                user_one.rating += 10
                user_two.rating -= 5

                user_one.wins_count += 1
                user_two.lose_count += 1
            if winner == 2:
                user_two.rating += 10
                user_one.rating -= 5

                user_two.wins_count += 1
                user_one.lose_count += 1

            db.add(user_one)
            db.add(user_two)

        return True

            
