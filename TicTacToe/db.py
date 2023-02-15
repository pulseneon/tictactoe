import os
from dotenv import load_dotenv
from sqlalchemy import BigInteger, Column, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

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
    lang = Column(String)

class Database:
    load_dotenv()
    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_name = os.getenv('DB_DATABASE')
    engine = create_engine(f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}")
    Base.metadata.create_all(bind=engine)   
    
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