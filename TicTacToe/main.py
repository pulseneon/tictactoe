import sys
import telebot
from handlers import Handlers
from env import TOKEN
from log import Logging

Logging.init_path()

try:
    bot = telebot.TeleBot(TOKEN)
except Exception as e:
    Logging.fatal(f"Не удалось запустить бота. Ошибка: {str(e)}")
    Logging.fatal('Выключаем приложение')
    sys.exit(1)


def main():
    Logging.info("Скрипт запущен")
    Handlers(bot)
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as ex:
            Logging.fatal(f"Критическая ошибка: {str(ex)}")


if __name__ == "__main__":
    main()
