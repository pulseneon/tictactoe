import os
#from language.langs import Language
#from keyboards import lang_keyboard
from db import Database
import telebot

# langs = Language()
# def get_string(string: str) -> str:
#     return langs.get_string(string)

# print(get_string("curr_chat_lansg"))
# print(get_string("curr_chat_lang"))
# #print(langs.get_languages())

# print(lang_keyboard)

bot = telebot.TeleBot(os.getenv('TOKEN'))
db = Database()

@bot.message_handler(commands=['start'])
def start(message):
    db.register_user(message)

bot.polling(none_stop=True)