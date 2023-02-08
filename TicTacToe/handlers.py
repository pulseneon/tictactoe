import telebot

class Handlers:
    def __init__(self, bot) -> None:
        self.bot = bot
        
        # handlers list
        bot.message_handler(commands=['start']) (self._handle_start)
        bot.message_handler(commands=['help']) (self._handle_help)

    def _handle_start(self, message):
        msg = self.bot.send_message(message.chat.id, f'Привет', parse_mode='markdown')

    def _handle_help(self, message):
        msg = self.bot.send_message(message.chat.id, f'use /start', parse_mode='markdown')
    