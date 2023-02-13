import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

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

    def register_user(self, user) -> True or False:
        pass