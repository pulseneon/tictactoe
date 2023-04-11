import datetime
import os

BOLD = '\33[1m'
ERROR = '\033[91m'
INFO = '\33[34m'
FATAL = '\033[93m'
RESET = '\033[0m'


def format_time_name():
    date = datetime.date
    now = datetime.datetime.now()
    time = now.strftime("%H-%M")
    return f'{date.today()} {time}'


def format_time_log():
    date = datetime.date
    now = datetime.datetime.now()
    time = now.strftime("%H:%M:%S")

    return f'[{date.today()} {time}]'


def generate_path():
    return f'./logs/log {format_time_name()}.txt'   #TicTacToe


class Logging:
    @staticmethod
    def init_path():
        log_file_path = generate_path()
        with open(file=log_file_path, mode='w+', encoding='utf-8') as f:
            f.write(f'{format_time_log()} [Info] Файл логгирования создан')

    @staticmethod
    def get_path():
        dir_path = "./logs/"      #TicTacToe
        files = os.listdir(dir_path)
        if files:
            files.sort(key=lambda x: os.path.getctime(os.path.join(dir_path, x)))
            latest_file = os.path.join(dir_path, files[-1])
            return latest_file

    @staticmethod
    def add_log(color, tag, message):
        with open(file=Logging.get_path(), mode='a', encoding='utf-8') as f:
            f.write(f'{format_time_log()} [{tag}] {message}\n')
        print(f'{BOLD}{color}{format_time_log()}[{tag}] {RESET}{message}')

    @staticmethod
    def info(message):
        Logging.add_log(INFO, 'Info', message)

    @staticmethod
    def warn(message):
        Logging.add_log(ERROR, 'Warn', message)

    @staticmethod
    def fatal(message):
        Logging.add_log(FATAL, 'Fatal', message)

    @staticmethod
    def debug(message):
        Logging.add_log(INFO, 'Debug', message)

    @staticmethod
    def error(message):
        Logging.add_log(ERROR, 'Error', message)
