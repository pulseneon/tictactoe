from TicTacToe.db import Database
from TicTacToe.env import ADMINS
from TicTacToe.keyboards import main_keyboard


# проверка на админа
def is_admin(id):
    for admin in ADMINS:
        if str(id) == admin:
            return True
    return False


class ACommands:
    def __init__(self, bot) -> None:
        self.bot = bot
        self.db = Database()

    # админ помощь команд
    def help(self, message):
        user_id = message.from_user.id
        if not is_admin(user_id):
            # лог что не админ команду ввел
            self.bot.send_message(message.chat.id, f'Воспользуйтесь клавиатурой ниже для работы',
                                  reply_markup=main_keyboard())
            return

        text = '''Список админ-команд:\n\n 
`/find_user {id}` - найти пользователя в бд
`/delete_user {id}` - удалить пользователя из бд
`/delete_game {user_id}` - закончить игру из бд через игрока
`/w {id} {text}` - написать в лс игроку
`/ad {text}` - рассылка игрокам
`/recreate_db` - пересоздать базу данных
`/help` - помощь
'''

        self.bot.send_message(user_id, text, parse_mode='markdown', reply_markup=None)

    # пересоздать бд
    def recreate_db(self, message):
        user_id = message.from_user.id
        if not is_admin(user_id):
            # лог что не админ команду ввел
            self.bot.send_message(message.chat.id, f'Воспользуйтесь клавиатурой ниже для работы',
                                  reply_markup=main_keyboard())
            return

        self.db.clear_database()
        self.bot.send_message(message.chat.id, f'База данных была очищена', parse_mode='markdown',
                              reply_markup=None)

    # найти пользователя в бд
    def find_user(self, message):
        user_id = message.from_user.id
        if not is_admin(user_id):
            # лог что не админ команду ввел
            self.bot.send_message(message.chat.id, f'Воспользуйтесь клавиатурой ниже для работы',
                                  reply_markup=main_keyboard())
            return

        message_args = message.text.split()
        find_user_id = message_args[1]
        find_user = self.db.find_user(find_user_id)

        if find_user is None:
            self.bot.send_message(message.chat.id, f'Такого игрока нет в базе данных',
                                  reply_markup=None)
            return

        in_game = f'нет' if find_user.game_id == -1 else f'да, игра номер {find_user.game_id}'

        text = f'''Пользователь  {find_user.username} [ID {find_user.user_id} (ID в бд: {find_user.id})]\n
Имя аккаунта: `{find_user.first_name} {find_user.last_name}`
Игр отыграно: `{find_user.games_count}`
Побед/Поражений: `{find_user.wins_count} / {find_user.lose_count}`
Рейтинг: `{find_user.rating}`
Язык профиля: `{find_user.lang}`
В игре: `{in_game}`
'''

        self.bot.send_message(message.chat.id, f'{text}', parse_mode='markdown',
                              reply_markup=None)

    # удалить игрока из бд
    def delete_user(self, message):
        user_id = message.from_user.id
        if not is_admin(user_id):
            # лог что не админ команду ввел
            self.bot.send_message(user_id, f'Воспользуйтесь клавиатурой ниже для работы',
                                  reply_markup=main_keyboard())
            return

        message_args = message.text.split()
        if len(message_args) < 2:
            self.bot.send_message(user_id, f'Ошибка: недостаточно аргументов для удаления игрока',
                                  reply_markup=None)
            return

        find_user_id = message_args[1]
        find_user = self.db.find_user(find_user_id)

        if find_user is None:
            self.bot.send_message(user_id, f'Ошибка: Игрока нет в бд',
                                  reply_markup=None)
            return

        self.db.delete_user(find_user_id)
        self.bot.send_message(user_id, f'Пользователь был удален из игры',
                              reply_markup=None)

    # удалить игру из бд
    def delete_game(self, message):
        user_id = message.from_user.id
        if not is_admin(user_id):
            # лог что не админ команду ввел
            self.bot.send_message(user_id, f'Воспользуйтесь клавиатурой ниже для работы',
                                  reply_markup=main_keyboard())
            return

        message_args = message.text.split()
        if len(message_args) < 2:
            self.bot.send_message(user_id, f'Ошибка: недостаточно аргументов для удаления игры',
                                  reply_markup=None)
            return

        find_user_id = message_args[1]
        find_user = self.db.find_user(find_user_id)

        if find_user is None:
            self.bot.send_message(user_id, f'Ошибка: Игрока нет в бд',
                                  reply_markup=None)
            return

        if find_user.game_id == -1:
            self.bot.send_message(user_id, f'Ошибка: Игрок и так вне игры',
                                  reply_markup=None)
            return

        self.db.cancel_game(find_user.game_id)
        self.bot.send_message(user_id, f'Игра была прекращена',
                              reply_markup=None)


    # написать кому-то в лс
    def send_msg(self, message):
        user_id = message.from_user.id
        if not is_admin(user_id):
            # лог что не админ команду ввел
            self.bot.send_message(message.chat.id, f'Воспользуйтесь клавиатурой ниже для работы',
                                  reply_markup=main_keyboard())
            return

        message_args = message.text.split()

        if len(message_args) < 3:
            self.bot.send_message(user_id, f'Ошибка: недостаточно аргументов для отправки сообщения',
                                  reply_markup=None)
            return

        find_user = self.db.find_user(message_args[1])

        if find_user is None:
            self.bot.send_message(user_id, f'Такого игрока нет в базе данных',
                                  reply_markup=None)
            return

        text = ' '.join(message_args[2:])
        self.bot.send_message(message_args[1], f'{text}')
        self.bot.send_message(user_id, f'Сообщение доставлено {find_user.username}. Текст сообщения: {text}')

    # рассылка всем
    def ad(self, message):
        user_id = message.from_user.id
        if not is_admin(user_id):
            # лог что не админ команду ввел
            self.bot.send_message(message.chat.id, f'Воспользуйтесь клавиатурой ниже для работы',
                                  reply_markup=main_keyboard())
            return

        message_args = message.text.split()

        if len(message_args) < 2:
            self.bot.send_message(user_id, f'Ошибка: недостаточно аргументов для отправки сообщения',
                                  reply_markup=None)
            return

        users = self.db.get_users()
        text = ' '.join(message_args[1:])
        idx = 0

        for user in users:
            self.bot.send_message(user.user_id, f'{text}')
            idx = idx + 1

        self.bot.send_message(user_id, f'Сообщение доставлено {idx} пользователям. Текст сообщения: {text}')
