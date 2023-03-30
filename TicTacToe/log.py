BOLD = '\33[1m'
RED = '\033[91m'
BLUE = '\33[34m'
RESET = '\033[0m'

class Logging:
    @staticmethod
    def _color_print(color, tag, str):
        print(f'{BOLD}{color}[{tag}] {RESET}{str}')

    @staticmethod
    def info(str):
        Logging._color_print(BLUE, 'Info', str)

    @staticmethod
    def warning(str):
        Logging._color_print(RED, 'Warning', str)