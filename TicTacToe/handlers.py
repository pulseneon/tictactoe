from db import Database
from keyboards import main_keyboard
from handle.commands import Commands
from handle.acommands import ACommands
from handle.callback import Callback


class Handlers:
    def __init__(self, bot) -> None:
        self.bot = bot
        self.commands = Commands(bot)
        self.acommands = ACommands(bot)
        self.db = Database()

        # user handlers list
        bot.message_handler(commands=['start'])(self.commands.start)
        bot.message_handler(commands=['menu'])(self.commands.menu)
        bot.message_handler(commands=['cancel_game'])(self.commands.cancel_game)

        # admin handlers list
        bot.message_handler(commands=['help'])(self.acommands.help)
        bot.message_handler(commands=['find_user'])(self.acommands.find_user)
        bot.message_handler(commands=['w'])(self.acommands.send_msg)
        bot.message_handler(commands=['ad'])(self.acommands.ad)
        bot.message_handler(commands=['delete_game'])(self.acommands.delete_game)
        bot.message_handler(commands=['delete_user'])(self.acommands.delete_user)
        bot.message_handler(commands=['recreate_db'])(self.acommands.recreate_db)
        bot.message_handler(commands=['users_count'])(self.acommands.users_count)

        @bot.callback_query_handler(func=lambda call: True)
        def callback(call):
            Callback(bot, call)

        # default handler
        bot.message_handler(content_types=["text"])(self._default_answer)
        bot.message_handler(content_types=['photo'])(self._default_answer)

    def _default_answer(self, message):
        check_on_reg = self.db.find_user(message.chat.id)
        if check_on_reg is None:
            self.commands.start(message)
            return

        msg = self.bot.send_message(message.chat.id, f'Воспользуйтесь клавиатурой ниже для работы',
                                    reply_markup=main_keyboard())
