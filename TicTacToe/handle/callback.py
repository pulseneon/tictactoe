# ! стоит добавить проверку всех действий не в игре ли пользователь и на выход из неё !

from db import Database
from keyboards import main_keyboard, choose_game_type , ready_keyaboard, gamefield
from language.langs import Language

class Callback:
    def __init__(self, bot, call) -> None:
        self.data = call
        self.bot = bot
        self.db = Database()
        self.langs = Language()
        self.lang = getattr(self.db.find_user(call.from_user.id), 'lang', 'en')

        self.get_str = self.langs.get_string_by_lang
        self.parse()

    def parse(self):
        command = self.data.data.split(':')[0]
        self.arg = self.data.data.split(':')[1]

        match command:
            case 'lang': # обработка работы с языком
                self._handle_lang()
            case 'main': # обработка нажатий главного меню
                self._handle_menu()
            case 'field':  # обработка хода игрока
                self._handle_field()
            case 'choose_game_type':
                self._handle_choose_game_type()
            case 'ready':
                self._ready_to_play()

    def _handle_lang(self):
        # УБРАТЬ ПОТОМ
        #self.db.clear_database() 
        # 
        self.db.register_user(self.data, self.arg)
        self.bot.send_message(chat_id=self.data.from_user.id, text=self.get_str('successfully_registered', self.arg), reply_markup = main_keyboard())

    def _handle_menu(self):
        match self.arg:
            case 'play':
                self.bot.send_message(chat_id=self.data.from_user.id, text=self.get_str('type_of_game', self.lang), reply_markup = choose_game_type())
            case 'play_with_bot':
                pass
            case 'stats':
                pass
            case 'rate':
                pass

    def _handle_field(self):
        
        match self.arg:
            case '1':
                # user_X = self.db.find_user_X (self.data.from_user.id)
                # check_for_movie = self.db.check_move_player_status(True)
                

                if (self.db.check_move_player_status() == True):
                    if (self.db.find_user_X (self.data.from_user.id)) == self.data.from_user.id:
                        self.bot.send_message(chat_id=self.data.from_user.id, text=f"Вы сделали ход" )




                        #finded_user = self.db.find_user_by_tag(message.text)

                        user_id = self.db.find_user_X(self.data.from_user.id)
                        
                        finded_user = self.db.find_user(user_id)

                        # game_id = finded_user.game_id

                        test1 = self.db.find_game_id_by_user(finded_user.user_id)

                        # test2 = self.db.find_game(test1)

                        

                        # self.db.update_field_value(test1,self.arg)
                        self.db.edit_gamefield(test1,self.arg,1)
                        # if(self.db.find_gamefield(self.arg)):
                        #     self.bot.send_message(chat_id=self.data.from_user.id, text=f"Эта клетка занята" ,reply_markup=gamefield())


                else:
                    self.bot.send_message(chat_id=self.data.from_user.id, text=f"Сейчас не ваш ход" ,reply_markup=gamefield())

    def _handle_choose_game_type(self):
        match self.arg:
            case 'random':
                pass
            case 'find':
                text = f'Упомяни игрока, с которым хочешь поиграть\n\nНапример: ```@username```'
                msg = self.bot.send_message(chat_id=self.data.from_user.id, text=text, parse_mode='MarkdownV2', reply_markup=None)
                self.bot.register_next_step_handler(msg, self.play_register)
    
    def _ready_to_play(self):
        
        # secondPlayer = self.db.find_user(self.data.from_user.id)
        # secPlayerID = secondPlayer.id
        # secPlayerID -=1

        # firstPlayer = self.db.find_user_by_id(secPlayerID)

        match self.arg:
            case 'true':
               #self.db.create_game(551414071,468078249) 
               game = self.db.create_game(551414071,468078249)

            #    self.db.add_to_game(game.game_id,551414071)
            #    self.db.add_to_game(game.game_id,468078249)

               self.bot.send_message(chat_id=551414071, text=f"Вы крестик, ваш ход" ,reply_markup=gamefield())

               self.bot.send_message(chat_id=468078249, text=f"Вы нолик, ожидайте пока игрок сделает ход" ,reply_markup=gamefield())

            case 'false':
                self.bot.send_message(chat_id=self.data.from_user.id, text=f"Вы отклонили предложение" ,reply_markup=main_keyboard())

    # !методы ниже нужно будет переорпеделить куда-то!

    # регистрация игры
    def play_register(self, message):
        # илья тут для работы, например поиска игрока ты пишешь например

        # дописать еще чтобы по ссылке можно было типо t.me/tgjdfg

        finded_user = self.db.find_user_by_tag(message.text)
        if (finded_user is None): # если он не найден 
            self.bot.send_message(chat_id=message.from_user.id, text=f"{message.text} Игрок не был найден.", reply_markup=main_keyboard())
            return

        
        if (finded_user.game_id is None): # если он не играет
            self.bot.send_message(chat_id = message.from_user.id, text=f" Отправлено приглашение пользователю ( {message.text} ) ", reply_markup=main_keyboard())
            self.bot.send_message(chat_id = finded_user.user_id, text=f" Вы были приглашены в игру (от " + str(message.from_user.username) + " )", reply_markup=ready_keyaboard())

            # firstPlayer = self.db.find_user(message.from_user.id)
            # secondPlayer = self.db.find_user(finded_user.user_id)

            

            return

   
        

        #self.bot.send_message(chat_id=message.from_user.id, text=f"{message.text} Отправлено приглашение пользователю "+message.text, reply_markup=main_keyboard())

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