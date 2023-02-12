import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from language.langs import Language

def lang_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    
    langs = Language()
    available_langs = langs.get_languages()
    available_langs_names = langs.get_languages_names()
    i = 0

    for item in available_langs:
        markup.add(InlineKeyboardButton(available_langs_names[i], callback_data=f'cb_{item}'))
        i=+1

    return markup