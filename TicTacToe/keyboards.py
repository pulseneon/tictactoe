#import types
from telebot import types
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

def gamefield():
    markup = InlineKeyboardMarkup()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton("1")
    item2 = types.KeyboardButton("2")
    item3 = types.KeyboardButton("3")
    item4 = types.KeyboardButton("4")
    item5 = types.KeyboardButton("5")
    item6 = types.KeyboardButton("6")
    item7 = types.KeyboardButton("7")
    item8 = types.KeyboardButton("8")
    item9 = types.KeyboardButton("9")
    markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9)

    return markup
