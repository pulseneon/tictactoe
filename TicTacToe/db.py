import datetime
import logging
import os
from dotenv import load_dotenv
from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer, String, create_engine, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker

from log import Logging
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

    def find_user(self, user_id) -> User:
        Session = sessionmaker(autoflush=False, bind=self.engine)
        with Session(autoflush=False, bind=self.engine) as db:
            user = db.query(User).filter(User.user_id == user_id).first()
            db.close()
            if user is not None:
                return user

        return None

 
    def find_game_id_by_user(self, user_id) -> Game:
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

    def find_user_by_tag(self, user_tag) -> User:
        Session = sessionmaker(autoflush=False, bind=self.engine)
        user_tag = user_tag[1:]  # убираем @

        with Session(autoflush=False, bind=self.engine) as db:
            user = db.query(User).filter(User.username == user_tag).first()
            db.close()
            if user is not None:
                return user
        return None

    def find_user_by_url(self, url) -> User:
        username = url.split('/')

        if len(username) < 3:
            return None

        Logging.debug(username)
        Session = sessionmaker(autoflush=False, bind=self.engine)
        with Session(autoflush=False, bind=self.engine) as db:
            user = db.query(User).filter(User.username == username[3]).first()
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

    def find_game(self, game_id) -> Game:
        Session = sessionmaker(autoflush=False, bind=self.engine)
        with Session(autoflush=False, bind=self.engine) as db:
            game = db.query(Game).filter(Game.id == game_id).first()
            db.close()
            if game is not None:
                return game
        return None

    def cancel_game(self, game_id) :
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


    def find_gamefield(self, gamefield_id) -> Gamefield:
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

    def update_move_player_status(self, game) -> object:
        Session = sessionmaker(autoflush=False, bind=self.engine)
        with Session(autoflush=False, bind=self.engine) as db:
            # game = db.query(Game).filter(Game.move_player == _move_player).first()
            if game is not None:
                with Session() as session:
                    game.move_player = not game.move_player
                    session.merge(game)
                    session.commit()
                
            return Game

    def edit_gamefield(self, gamefield_id, field_obj, value) -> object:
        field = self.find_gamefield(gamefield_id)
        # field.field_obj = value
        Session = sessionmaker(autoflush=False, bind=self.engine)
        match field_obj:
                case '1':
                    with Session() as session:
                        field.field1 = value
                        session.merge(field)
                        session.commit()

                case '2':
                    with Session() as session:
                        field.field2 = value
                        session.merge(field)
                        session.commit()

                case '3':
                    with Session() as session:
                        field.field3 = value
                        session.merge(field)
                        session.commit()

                case '4':
                    with Session() as session:
                        field.field4 = value
                        session.merge(field)
                        session.commit()

                case '5':
                    with Session() as session:
                        field.field5 = value
                        session.merge(field)
                        session.commit()

                case '6':
                    with Session() as session:
                        field.field6 = value
                        session.merge(field)
                        session.commit()

                case '7':
                    with Session() as session:
                        field.field7 = value
                        session.merge(field)
                        session.commit()

                case '8':
                    with Session() as session:
                        field.field8 = value
                        session.merge(field)
                        session.commit()

                case '9':
                    with Session() as session:
                        field.field9 = value
                        session.merge(field)
                        session.commit()
                

        return field


    def get_gamefield(self, gamefield_id, field_obj) -> object:
        field = self.find_gamefield(gamefield_id)
        
        Session = sessionmaker(autoflush=False, bind=self.engine)
        match field_obj:
                case '1':
                    with Session() as session:
                        if field.field1 is not 0:
                            return field.field1

                case '2':
                    with Session() as session:
                        if field.field2 is not 0:
                            return field.field2
                
                case '3':
                    with Session() as session:
                        if field.field3 is not 0:
                            return field.field3

                case '4':
                    with Session() as session:
                        if field.field4 is not 0:
                            return field.field4 

                case '5':
                    with Session() as session:
                        if field.field5 is not 0:
                            return field.field5

                case '6':
                    with Session() as session:
                        if field.field6 is not 0:
                            return field.field6

                case '7':
                    with Session() as session:
                        if field.field7 is not 0:
                            return field.field7

                case '8':
                    with Session() as session:
                        if field.field8 is not 0:
                            return field.field8

                case '9':
                    with Session() as session:
                        if field.field9 is not 0:
                            return field.field9

        return 0

    def check_win(self,gamefield_id,player) ->object:
        
        win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]

        fields = [self.get_gamefield(gamefield_id,'1'),
        self.get_gamefield(gamefield_id,'2'),
        self.get_gamefield(gamefield_id,'3'),
        self.get_gamefield(gamefield_id,'4'),
        self.get_gamefield(gamefield_id,'5'),
        self.get_gamefield(gamefield_id,'6'),
        self.get_gamefield(gamefield_id,'7'),
        self.get_gamefield(gamefield_id,'8'),
        self.get_gamefield(gamefield_id,'9')]

        for index in win_conditions:
            if fields[index[0]] == player and fields[index[1]] == player and fields[index[2]] == player:
                return True       
        return False


    def check_draw(self,gamefield_id) ->object:

        fields = [self.get_gamefield(gamefield_id,'1'),
        self.get_gamefield(gamefield_id,'2'),
        self.get_gamefield(gamefield_id,'3'),
        self.get_gamefield(gamefield_id,'4'),
        self.get_gamefield(gamefield_id,'5'),
        self.get_gamefield(gamefield_id,'6'),
        self.get_gamefield(gamefield_id,'7'),
        self.get_gamefield(gamefield_id,'8'),
        self.get_gamefield(gamefield_id,'9')]

        for index in fields:
            if index == 0:
                return False 
        return True

    def calc_rating(self,player_id) -> object:
        rating_list = []
        index = 1
        while True:
            user = self.get_users_by_id(index)
            if user is not None:
                rating_list.append(user)
                index += 1
            else:
                break
        
        rating_list.sort(key = lambda x: x.rating,reverse=True)

        return rating_list

    def get_users_by_id(self,index) -> User:
        Session = sessionmaker(autoflush=False, bind=self.engine)
        with Session(autoflush=False, bind=self.engine) as db:
            user = db.query(User).filter(User.id == index).first()
            db.close()
            if user is not None:
                return user
        return None

    def get_users(self):
        Session = sessionmaker(autoflush=False, bind=self.engine)
        with Session() as session:
            return session.query(User).all()

    def delete_user(self, user_id: int):
        Session = sessionmaker(autoflush=False, bind=self.engine)
        with Session() as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                session.delete(user)
                session.commit()
                return True
            return False

    def calc_game_result(self, user_id: int):
        Session = sessionmaker(autoflush=False, bind=self.engine)
        with Session() as session:
            lose_user = session.query(User).filter(User.user_id == user_id).first()
            game = self.find_game(lose_user.game_id)

            if game.first_player_id == user_id:
                win_user = session.query(User).filter(User.user_id == game.second_player_id).first()
            else:
                win_user = session.query(User).filter(User.user_id == game.first_player_id).first()


            lose_user.lose_count = lose_user.lose_count + 1
            lose_user.rating = lose_user.rating - 5
            lose_user.games_count = lose_user.games_count + 1
            win_user.games_count = win_user.games_count + 1
            win_user.wins_count = win_user.wins_count + 1
            win_user.rating = win_user.rating + 5

            session.commit()

    def finish_game(self, first_player_id, second_player_id, winner):
        try:
            Session = sessionmaker(autoflush=False, bind=self.engine)
            with Session() as session:
                # Find the user objects for the two players
                first_player_obj = self.find_user(first_player_id)
                second_player_obj = self.find_user(second_player_id)

                # Update the game statistics for the two players
                first_player_obj.game_id = -1
                second_player_obj.game_id = -1

                first_player_obj.games_count += 1
                second_player_obj.games_count += 1

                if winner == 1:
                    first_player_obj.wins_count += 1
                    second_player_obj.lose_count += 1
                elif winner == 2:
                    second_player_obj.wins_count += 1
                    first_player_obj.lose_count += 1

                # Update the ratings of the two players
                rating_change = 10
                if winner == 0:
                    rating_change = 0
                elif winner == 2:
                    rating_change *= -1
                first_player_obj.rating += rating_change
                second_player_obj.rating -= rating_change

                # Update the user objects in the database
                session.add_all([first_player_obj, second_player_obj])
                session.commit()
        except Exception as ex:
            Logging.fatal(f'Ошибка завершения игры. Ошибка: {str(ex)}')
