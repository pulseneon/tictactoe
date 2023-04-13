# import types
from telebot import types
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from db import Database
from language.langs import Language

def main_keyboard(user_id):
    db = Database()
    markup = InlineKeyboardMarkup()
    markup.row_width = 3

    user_obj = db.find_user(user_id)

    if user_obj.game_id == -1:
        markup.add(InlineKeyboardButton('Играть', callback_data=f'main:play')) # напишите его nickname или telegram id
    else:
        markup.add(InlineKeyboardButton('Вернуться к игре', callback_data=f'main:return_play'))
        markup.add(InlineKeyboardButton('Покинуть игру', callback_data=f'main:cancel_game'))
    markup.add(InlineKeyboardButton('Статистика', callback_data=f'main:stats')) # статистика профиля
    markup.add(InlineKeyboardButton('Рейтинг', callback_data=f'main:rate')) # рейтинг всех игроков 
    '''
    Пример:
    1. Lesnov  - 500 MMR
    2. Rudnev - 480 MMR
    3. example - 100 MMR
    4. example - 100 MMR
    5. example - 100 MMR
    5. example - 100 MMR
    5. example - 100 MMR
    5. example - 100 MMR
    ...
    201. {ник_пользователя} - {его} ММР
    '''
    markup.add(InlineKeyboardButton('Настройки', callback_data=f'main:settings')) # сменить язык / сброс статистики
    return markup

def choose_game_type():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Играть с другом', callback_data=f'choose_game_type:find'))
    markup.add(InlineKeyboardButton('Играть с рандомным игроком', callback_data=f'choose_game_type:random'))
    
    return markup

def lang_keyboard(type = 0):
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    
    langs = Language()
    available_langs = langs.get_languages()
    available_langs_names = langs.get_languages_names()
    i = 0

    for item in available_langs:
        if type == 0:
            markup.add(InlineKeyboardButton(available_langs_names[i], callback_data=f'lang:{item}'))
        else:
            markup.add(InlineKeyboardButton(available_langs_names[i], callback_data=f'change_lang:{item}'))
        i+=1

    return markup

def cancel_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Отмена', callback_data=f'cancel_game:true'))

    return markup

def ready_keyaboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Готов', callback_data=f'ready:true')) 
    markup.add(InlineKeyboardButton('Не готов', callback_data=f'ready:false'))
    
    return markup

def gamefield():
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton("1", callback_data=f'field:1')
    item2 = types.InlineKeyboardButton("2", callback_data=f'field:2')
    item3 = types.InlineKeyboardButton("3", callback_data=f'field:3')
    item4 = types.InlineKeyboardButton("4", callback_data=f'field:4')
    item5 = types.InlineKeyboardButton("5", callback_data=f'field:5')
    item6 = types.InlineKeyboardButton("6", callback_data=f'field:6')
    item7 = types.InlineKeyboardButton("7", callback_data=f'field:7')
    item8 = types.InlineKeyboardButton("8", callback_data=f'field:8')
    item9 = types.InlineKeyboardButton("9", callback_data=f'field:9')
    leave = types.InlineKeyboardButton("Сдаться", callback_data=f'field:leave')
    markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, leave)

    return markup

def settings_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Сменить язык', callback_data=f'settings:change_lang'))
    markup.add(InlineKeyboardButton('Сбросить статистику', callback_data=f'settings:reset_stats'))
    markup.add(InlineKeyboardButton('Назад', callback_data=f'settings:back'))

    return markup