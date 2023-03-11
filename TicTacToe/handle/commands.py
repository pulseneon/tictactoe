from language.langs import Language
from keyboards import lang_keyboard, main_keyboard

# хз откуда она но она есть
# def get_string(string: str) -> str:
#     return langs.get_string(string)

class Commands:
    def __init__(self, bot) -> None:
        self.bot = bot
        self.langs = Language()

    # /start
    def start(self, message):
        get_str = self.langs.get_string_by_lang
        text = f'{get_str("language_suggestion", "ru")}\n\n{get_str("language_suggestion", "en")}'
        msg = self.bot.send_message(message.chat.id, text, parse_mode='markdown', reply_markup=lang_keyboard())

    # /menu вывод меню мало ли что 
    def menu(self, message):
        text = 'Было открыто главное меню'
        msg = self.bot.send_message(message.chat.id, text, parse_mode='markdown', reply_markup=main_keyboard())