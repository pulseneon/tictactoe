import telebot
from keyboards import lang_keyboard
from language.langs import Language

langs = Language()
def get_string(string: str) -> str:
    return langs.get_string(string)

class Handlers:
    def __init__(self, bot) -> None:
        self.bot = bot
        
        # handlers list
        bot.message_handler(commands=['start']) (self._handle_start)
        bot.message_handler(commands=['help']) (self._handle_help)

    def _handle_start(self, message):
        msg = self.bot.send_message(message.chat.id, f'{langs.get_string_by_lang("language_suggestion", "ru")}\n\n{langs.get_string_by_lang("language_suggestion", "en")}', parse_mode='markdown', reply_markup=lang_keyboard())

    def _handle_help(self, message):
        msg = self.bot.send_message(message.chat.id, f'use /start', parse_mode='markdown')