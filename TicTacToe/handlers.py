import telebot
from keyboards import lang_keyboard, gamefield
from language.langs import Language
from db import Database

langs = Language()
db = Database()
def get_string(string: str) -> str:
    return langs.get_string(string)

class Handlers:
    def __init__(self, bot) -> None:
        self.bot = bot
        
        # handlers list
        bot.message_handler(commands=['start']) (self._handle_start)
        bot.message_handler(commands=['help']) (self._handle_help)
        bot.message_handler(commands=['play']) (self._handle_play)
        # (self._handle_register) # исправить под все языки мира циклом
        @bot.callback_query_handler(func=lambda call: True)
        def callback(call):
            self._handle_register(call)

    def _handle_start(self, message):
        msg = self.bot.send_message(message.chat.id, f'{langs.get_string_by_lang("language_suggestion", "ru")}\n\n{langs.get_string_by_lang("language_suggestion", "en")}', parse_mode='markdown', reply_markup=lang_keyboard())

    def _handle_help(self, message):
        msg = self.bot.send_message(message.chat.id, f'use /start', parse_mode='markdown')
        
    def _handle_play(self, message):
        playerX = message.from_user.id
        playerO = message.text.split(' ')[1]
    
        first_player = db.find_user(playerX)
        if first_player.game_id is not None:
            self.bot.send_message(chat_id=playerX, text="Извините вы в игре")
            return

        second_player = db.find_user(playerO)
        if second_player is None:
            self.bot.send_message(chat_id=playerX, text="Игрок не найден в базе данных")
            return

        if second_player.game_id is not None:
            self.bot.send_message(chat_id=playerX, text="Извините он играет")
            return
        
        game = db.create_game(playerX, playerO)
        self.bot.send_message(chat_id=playerX, text="Ты крестик", reply_markup=gamefield())
        self.bot.send_message(chat_id=playerO, text="Ты нолик", reply_markup=gamefield())

    def _handle_register(self, data):
        print(data.data) # cb_ru
        command = data.data.split('_')[0]
        if (command == 'cb'):
            db.register_user(data, 'ru')
            self.bot.send_message(chat_id=data.from_user.id, text="Вы зарегистрированы")

