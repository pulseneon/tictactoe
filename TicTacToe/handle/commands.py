from db import Database
from language.langs import Language
from keyboards import lang_keyboard, main_keyboard

# хз откуда она но она есть
# def get_string(string: str) -> str:
#     return langs.get_string(string)


class Commands:
    def __init__(self, bot) -> None:
        self.bot = bot
        self.langs = Language()
        self.db = Database()

    # /start
    def start(self, message):
        get_str = self.langs.get_string_by_lang
        text = f'{get_str("language_suggestion", "ru")}\n\n{get_str("language_suggestion", "en")}'
        msg = self.bot.send_message(message.chat.id, text, parse_mode='markdown', reply_markup=lang_keyboard())

    # /menu вывод меню мало ли что
    def menu(self, message):
        text = 'Было открыто главное меню'
        msg = self.bot.send_message(message.chat.id, text, parse_mode='markdown', reply_markup=main_keyboard())

    def exit(self, message):
        try:
            this_user = self.db.find_user(message.from_user.id)
            self.db.calc_game_result(this_user.user_id)

            players_id = self.db.cancel_game(this_user.game_id)
            for player_id in players_id:
                self.bot.send_message(chat_id=player_id, text=f"Вы завершили игру",
                                      reply_markup=main_keyboard())
        except Exception as ex:
            self.bot.send_message(chat_id=this_user.user_id, text=f"Произошла непредвиденная ошибка.",
                                  reply_markup=main_keyboard())
            print(f'Произошла ошибка: {str(ex)}')