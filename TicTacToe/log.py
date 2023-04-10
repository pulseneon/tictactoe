import datetime

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
    return f'logs/log {format_time_name()}.txt'


class Logging:
    log_file_path = None

    @staticmethod
    def init_path():
        Logging.log_file_path = generate_path()
        print(Logging.log_file_path)

    @staticmethod
    def add_log(color, tag, message):
        with open(file=Logging.log_file_path, mode='w', encoding='utf-8') as f:
            f.seek(0)
            f.write(f'{format_time_log()} [{tag}] {message}')
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
