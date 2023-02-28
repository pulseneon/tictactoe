from commands import Commands

class ACommans(Commands):
    def __init__(self, bot) -> None:
        super().__init__(bot)

    # админ помощь команд
    def help(self):
        pass

    # пересоздать бд
    def recreate_db(self):
        pass

    # найти пользователя в бд
    def find_user(self):
        pass

    # удалить игрока из бд
    def delete_user(self):
        pass

    # удалить игру из бд
    def delete_game(self):
        pass

    # написать кому-то в лс
    def mailing(self):
        pass

    # рассылка всем
    def ad(self):
        pass