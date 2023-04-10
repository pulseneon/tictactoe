import sys
import telebot
from handlers import Handlers
from env import TOKEN
from log import Logging

try:
    bot = telebot.TeleBot(TOKEN)
except Exception as e:
    Logging.fatal(f"Не удалось запустить бота. Ошибка: {str(e)}")
    Logging.fatal('Выключаем приложение')
    sys.exit(1)


def main():
    Handlers(bot)
    Logging.init_path()
    Logging.info("Скрипт запущен")
    bot.polling(none_stop=True)


if __name__ == "__main__":
    main()
