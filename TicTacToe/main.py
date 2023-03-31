import sys
import telebot
from handlers import Handlers
from env import TOKEN
from TicTacToe.log import Logging

try:
    bot = telebot.TeleBot(TOKEN)
except Exception as e:
    # write log
    sys.exit(1)


def main():
    Handlers(bot)
    Logging().info("Script start")
    bot.polling(none_stop=True)


if __name__ == "__main__":
    main()
