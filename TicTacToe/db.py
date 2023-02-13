import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

from TicTacToe.models.user import User

class Base(DeclarativeBase): pass

class Database:
    def __init__(self) -> None:
        load_dotenv()
        db_user = os.getenv('DB_USER')
        db_pass = os.getenv('DB_PASSWORD')
        db_host = os.getenv('DB_HOST')
        db_name = os.getenv('DB_NAME')
        
        postgresql_database = f'postgresql://{db_user}:{db_pass}@{db_host}/{db_name}'

        engine = create_engine(postgresql_database)

        Base.metadata.create_all(bind=engine) # create db ?
        Session = sessionmaker(autoflush=False, bind=engine)

    def register_user(self, message, selected_lang) -> True or False:
        with self.Session(autoflush=False, bind=self.engine) as db:
            new_user = User(
                user_id = message.from_user.id,
                username = message.from_user.username,
                firstname = message.from_user.first_name,
                lastname = message.from_user.last_name,
                games_count = 0,
                lose_count = 0,
                wins_count = 0,
                lang = selected_lang
            )
            
            db.add(new_user)
            db.commit()
            print(new_user.id)
        return True