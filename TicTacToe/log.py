import datetime

BOLD = '\33[1m'
RED = '\033[91m'
BLUE = '\33[34m'
RESET = '\033[0m'


def format_time():
    date = datetime.date
    time = datetime.datetime.now()
    return f'{date.today()} {time.hour}-{time.minute}'


def generate_path():
    return f'./TicTacToe/logs/log {format_time()}.txt'


class Logging:
    def __init__(self):
        self.log_file_path = generate_path()

    def add_log(self, color, tag, message):
        with open(file=self.log_file_path, mode='w', encoding='utf-8') as f:
            f.seek(0)
            f.write(f'{format_time()} [{tag}] {message}')
        print(f'{BOLD}{color}[{tag}] {RESET}{message}')

    def info(self, message):
        self.add_log(BLUE, 'Info', message)

    def warning(self, message):
        self.add_log(RED, 'Warning', message)