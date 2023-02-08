import os
import sys
import telebot
from dotenv import load_dotenv

from handlers import Handlers

try:
    load_dotenv()
    bot = telebot.TeleBot(os.getenv('TOKEN'))
except Exception as e:
    # write log
    sys.exit(1)

def main():
    add_handlers = Handlers(bot)
    bot.polling(none_stop=True)

if __name__ == "__main__":
    main()