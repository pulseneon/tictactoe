from keyboards import lang_keyboard, gamefield, main_keyboard
from handle.commands import Commands
from handle.callback import Callback

class Handlers:
    def __init__(self, bot) -> None:
        self.bot = bot
        commands = Commands(bot)
        
        # handlers list
        bot.message_handler(commands=['start']) (commands.start)
        bot.message_handler(commands=['menu']) (commands.menu)

        @bot.callback_query_handler(func=lambda call: True)
        def callback(call):
            Callback(bot, call)

        # default handler
        bot.message_handler(content_types=["text"]) (self._default_answer)
        bot.message_handler(content_types = ['photo']) (self._default_answer)
    
    def _default_answer(self, message):
        msg = self.bot.send_message(message.chat.id, f'Воспользуйтесь клавиатурой ниже для работы', reply_markup = main_keyboard())