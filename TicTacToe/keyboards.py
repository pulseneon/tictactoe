# import types
from telebot import types
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from db import Database
from language.langs import Language

def main_keyboard(user_id):
    db = Database()
    lang = Language()

    markup = InlineKeyboardMarkup()
    markup.row_width = 3

    user_obj = db.find_user(user_id)
    get_str = lang.get_string_by_lang

    if user_obj.game_id == -1:
        markup.add(InlineKeyboardButton(get_str('playB',user_obj.lang), callback_data=f'main:play')) # напишите его nickname или telegram id
    else:
        markup.add(InlineKeyboardButton(get_str('backToGameB',user_obj.lang), callback_data=f'main:return_play'))
        markup.add(InlineKeyboardButton(get_str('leaveTheGameB',user_obj.lang), callback_data=f'main:cancel_game'))
    markup.add(InlineKeyboardButton(get_str('statisticsB',user_obj.lang), callback_data=f'main:stats')) # статистика профиля
    markup.add(InlineKeyboardButton(get_str('ratingB',user_obj.lang), callback_data=f'main:rate')) # рейтинг всех игроков 
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
    markup.add(InlineKeyboardButton(get_str('settingsB',user_obj.lang), callback_data=f'main:settings')) # сменить язык / сброс статистики
    return markup

def choose_game_type(user_id):
    db = Database()
    lang = Language()

    user_obj = db.find_user(user_id)
    get_str = lang.get_string_by_lang

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(get_str('playWithFriendB',user_obj.lang), callback_data=f'choose_game_type:find'))
    markup.add(InlineKeyboardButton(get_str('playWithRandomPlayerB',user_obj.lang), callback_data=f'choose_game_type:random'))
    
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

def cancel_keyboard(user_id):
    db = Database()
    lang = Language()

    user_obj = db.find_user(user_id)
    get_str = lang.get_string_by_lang

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(get_str('cancelB',user_obj.lang), callback_data=f'cancel_game:true'))

    return markup

def ready_keyaboard(user_id):
    db = Database()
    lang = Language()

    user_obj = db.find_user(user_id)
    get_str = lang.get_string_by_lang

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(get_str('readyB',user_obj.lang), callback_data=f'ready:true')) 
    markup.add(InlineKeyboardButton(get_str('notReadyB',user_obj.lang), callback_data=f'ready:false'))
    
    return markup

def gamefield(user_id):
    db = Database()
    lang = Language()

    user_obj = db.find_user(user_id)
    get_str = lang.get_string_by_lang

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
    leave = types.InlineKeyboardButton(get_str('giveUpB',user_obj.lang), callback_data=f'field:leave')
    markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, leave)

    return markup

def settings_keyboard(user_id):
    db = Database()
    lang = Language()

    user_obj = db.find_user(user_id)
    get_str = lang.get_string_by_lang

    markup = types.InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(get_str('changeTheLanguage',user_obj.lang), callback_data=f'settings:change_lang'))
    markup.add(InlineKeyboardButton(get_str('resetStatisticsB',user_obj.lang), callback_data=f'settings:reset_stats'))
    markup.add(InlineKeyboardButton(get_str('backB',user_obj.lang), callback_data=f'settings:back'))

    return markup