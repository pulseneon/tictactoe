# ! стоит добавить проверку всех действий не в игре ли пользователь и на выход из неё !
from db import Database
from keyboards import main_keyboard

class Callback:
    def __init__(self, bot, call) -> None:
        self.data = call
        self.bot = bot
        self.db = Database()
        self.parse()

    def parse(self):
        command = self.data.data.split(':')[0]
        self.arg = self.data.data.split(':')[1]

        # обработка работы с языком
        if command == 'lang':
            self._handle_lang()

        # обработка нажатий главного меню
        elif command == 'main':
            self._handle_menu()

        # обработка хода игрока
        elif command == 'field':
            self._handle_field()

    # исправить под все языки мира циклом
    def _handle_lang(self):
        self.db.register_user(self.data, 'ru')
        self.bot.send_message(chat_id=self.data.from_user.id, text="Вы зарегистрированы", reply_markup = main_keyboard())

    def _handle_menu(self):
        if (self.arg == 'play_with_user'):
            text = f'Упомяни игрока, с которым хочешь поиграть\n\nНапример: ```@username```'
            msg = self.bot.send_message(chat_id=self.data.from_user.id, text=text, parse_mode='MarkdownV2', reply_markup=None)
            self.bot.register_next_step_handler(msg, self.play_register)

    def _handle_field(self):
        pass
    
    # !методы ниже нужно будет переорпеделить куда-то!

    # регистрация игры
    def play_register(self, message):
        # илья тут для работы, например поиска игрока ты пишешь например
        finded_user = self.db.find_user_by_tag(message.text)
        if (finded_user is None): # если он не найден 
            self.bot.send_message(chat_id=message.from_user.id, text=f"{message.text} игрок не был найден.", reply_markup=main_keyboard())
            return

        # если не вернул ретенр значит он найден
        # проверяем играет ли он через finded.user.game_id если он тоже None то не играет иначе выводим ошибку пусть доиграет

        # если не играет то отправляем сообщения об успешной отправке предложения поиграть 
        # и finded.user.user_id тоже отправляем предложение поиграть и ждем их ответы
        # создаем игру и закидываем туда начавшего игру и при нажатии буду играть на клавиатуре ready_keyboard() приглашенным
        # скинуть им двоим приглос на игру и хукать уже непосредственно клавиатуру 3х3 и просчитывать поочередно ходы

        '''
        playerX = message.from_user.id
    #     playerO = message.text.split(' ')[1]
    
    #     first_player = db.find_user(playerX)
    #     if first_player.game_id is not None:
    #         self.bot.send_message(chat_id=playerX, text="Извините вы в игре")
    #         return

    #     second_player = db.find_user(playerO)
    #     if second_player is None:
    #         self.bot.send_message(chat_id=playerX, text="Игрок не найден в базе данных")
    #         return

    #     if second_player.game_id is not None:
    #         self.bot.send_message(chat_id=playerX, text="Извините он играет")
    #         return
        
    #     game = db.create_game(playerX, playerO)
    #     self.bot.send_message(chat_id=playerX, text="Ты крестик", reply_markup = gamefield())
    #     self.bot.send_message(chat_id=playerO, text="Ты нолик", reply_markup = gamefield())
        '''