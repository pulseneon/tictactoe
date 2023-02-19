import os
from dotenv import load_dotenv

import psycopg2
from sqlalchemy import create_engine
#from language.langs import Language
#from keyboards import lang_keyboard
from db import Database
import telebot
from sqlalchemy.orm import DeclarativeBase

# langs = Language()
# def get_string(string: str) -> str:
#     return langs.get_string(string)

# print(get_string("curr_chat_lansg"))
# print(get_string("curr_chat_lang"))
# #print(langs.get_languages())

# print(lang_keyboard)

load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))
print(os.getenv('TOKEN'))
db = Database()

# db.clear_database()

@bot.message_handler(commands=['start'])
def start(message):
    print()

bot.polling(none_stop=True)

# print(db.find_game(1).created_on)
# print(db.find_gamefield(db.find_game(1).gamefield_id).field1)



# conn = psycopg2.connect(dbname="postgres", user="postgres", password="12345", host="127.0.0.1")
# cursor = conn.cursor()
# print("подключились")
# cursor.close()

# url = 'postgresql://postgres:12345@localhost/postgres'
# engine = create_engine(url)
# class Base(DeclarativeBase): pass
# Base.metadata.create_all(bind=engine) # create db ?