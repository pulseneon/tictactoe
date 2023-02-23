import sys
import telebot
from handlers import Handlers
from env import TOKEN

try:
    bot = telebot.TeleBot(TOKEN)
except Exception as e:
    # write log
    sys.exit(1)

def main():
    add_handlers = Handlers(bot)
    bot.polling(none_stop=True)

if __name__ == "__main__":
    main()