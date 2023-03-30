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
    rating = Column(Integer, default=100)  # at least zero initially 100 and give 5 for win
    lang = Column(String)
    game_id = Column(Integer, nullable=False, default=-1)  # if -1 => user in menu


class Game(Base):
    __tablename__ = "game"
    id = Column(Integer, primary_key=True, index=True)
    gamefield_id = Column(Integer, ForeignKey("gamefield.id"), nullable=False)
    first_player_id = Column(BigInteger, nullable=False)  # изначально крестики
    second_player_id = Column(BigInteger, nullable=False)  # изначально нолики
    move_player = Column(Boolean, nullable=False, default=True)
    created_on = Column(DateTime(timezone=True), default=func.now())
    # game_id = Column(Integer, primary_key=True, index=True)


class Gamefield(Base):
    __tablename__ = "gamefield"
    game = relationship("Game")  # 0 - пусто, 1 - крестик, 2 - нолик
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
                user_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                games_count=0,
                lose_count=0,
                wins_count=0,
                lang=selected_lang
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

    def find_user_X(self, _id) -> object:
        Session = sessionmaker(autoflush=False, bind=self.engine)
        with Session(autoflush=False, bind=self.engine) as db:
            user_X = db.query(Game).filter(Game.first_player_id == _id).first()
            db.close()
            if user_X is not None:
                return user_X.first_player_id

        return None

    def find_game_id_by_user(self, user_id) -> object:
        Session = sessionmaker(autoflush=False, bind=self.engine)
        with Session(autoflush=False, bind=self.engine) as db:
            game_id = db.query(Game).filter(Game.first_player_id == user_id).first()
            db.close()
            if game_id is not None:
                return game_id.gamefield_id
        return None

    def add_to_game(self, game_id, user_id) -> object:
        user = self.find_user(user_id)
        user.game_id = game_id
        with sessionmaker(autoflush=False, bind=self.engine)() as db:
            db.merge(user)

        db.close()
        return user

    def find_user_by_tag(self, user_tag) -> object:
        Session = sessionmaker(autoflush=False, bind=self.engine)
        user_tag = user_tag[1:]  # убираем @

        with Session(autoflush=False, bind=self.engine) as db:
            user = db.query(User).filter(User.username == user_tag).first()
            db.close()
            if user is not None:
                return user
        return None

    def create_game(self, user_id_1, user_id_2) -> Game:
        null_game_id = -1
        if self.find_user(user_id_1).game_id != null_game_id or \
                self.find_user(user_id_2).game_id != null_game_id:
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
            db.commit()

            print(new_game.id)

            # refresh users game_id
            user_one = db.query(User).filter(User.user_id == user_id_1).first()
            user_two = db.query(User).filter(User.user_id == user_id_2).first()

            user_one.game_id = new_game.id
            user_two.game_id = new_game.id
            db.flush()

            db.commit()
            return new_game

    def find_game(self, game_id) -> object:
        Session = sessionmaker(autoflush=False, bind=self.engine)
        with Session(autoflush=False, bind=self.engine) as db:
            game = db.query(Game).filter(Game.id == game_id).first()
            db.close()
            if game is not None:
                return game
        return None

    def cancel_game(self, game_id) -> []:
        return_list = []

        Session = sessionmaker(autoflush=False, bind=self.engine)
        with Session(autoflush=False, bind=self.engine) as db:
            game = db.query(Game).filter(Game.id == game_id).first()

            user_one = db.query(User).filter(User.user_id == game.first_player_id).first()
            user_two = db.query(User).filter(User.user_id == game.second_player_id).first()

            return_list.append(user_one.user_id)
            return_list.append(user_two.user_id)

            user_one.game_id = -1
            user_two.game_id = -1

            db.commit()

            return return_list


    def find_gamefield(self, gamefield_id) -> object:
        Session = sessionmaker(autoflush=False, bind=self.engine)
        with Session(autoflush=False, bind=self.engine) as db:
            gamefield = db.query(Gamefield).filter(Gamefield.id == gamefield_id).first()
            db.close()
            if gamefield is not None:
                return gamefield
        return None

    def check_move_player_status(self) -> object:
        Session = sessionmaker(autoflush=False, bind=self.engine)
        with Session(autoflush=False, bind=self.engine) as db:
            player = db.query(Game).filter(Game.move_player).first()
            db.close()
            if player.move_player is not None:
                return player.move_player

            return False

    def update_move_player_status(self, _move_player) -> object:
        Session = sessionmaker(autoflush=False, bind=self.engine)
        with Session(autoflush=False, bind=self.engine) as db:
            game = db.query(Game).filter(Game.move_player == _move_player).first()
            if game is not None:
                game.move_player = not _move_player
                db.commit()
                return True
            return False

    def update_gamefield(self, _id, player) -> object:  # если 1 то крестик, если 2 то нолик
        Session = sessionmaker(autoflush=False, bind=self.engine)
        with Session(autoflush=False, bind=self.engine) as db:
            match _id:
                case '1':
                    game_field = db.query(Gamefield).filter(Gamefield.field1 == 0).first()

                    if game_field.field1 == 0:
                        db.field1 = player
                        db.commit()
                        return
                    return False

    def edit_gamefield(self, gamefield_id, field_obj, value) -> object:
        field = self.find_gamefield(gamefield_id)
        field.field_obj = value
        Session = sessionmaker(autoflush=False, bind=self.engine)
        with Session() as session:
            session.merge(field)
            session.commit()

        return field

    # def get_gamefield_id(self):
    #     Session = sessionmaker(autoflush=False, bind=self.engine)
    #     with Session(autoflush=False, bind=self.engine) as db:
    #         gamefield_id = db.query(Gamefield).filter(Gamefield.id  ...).first()
    #         return gamefield_id.

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

            user_one.games_count = user_one.games_count + 1
            user_two.games_count = user_two.games_count + 1

            if winner == 1:
                user_one.rating = user_one.rating + 10
                user_two.rating = user_two.rating - 5

                user_one.wins_count = user_one.wins_count + 1
                user_two.lose_count = user_two.wins_count + 1
            if winner == 2:
                user_two.rating = user_two.rating + 10
                user_one.rating = user_one.rating - 5

                user_two.wins_count = user_two.wins_count + 1
                user_one.lose_count = user_one.wins_count + 1

            db.add(user_one)
            db.add(user_two)

        return True
