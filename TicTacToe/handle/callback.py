# ! стоит добавить проверку всех действий не в игре ли пользователь и на выход из неё !

from db import Database
from keyboards import main_keyboard, choose_game_type, ready_keyaboard, gamefield, cancel_keyboard
from language.langs import Language
from log import Logging


class Callback:
    def __init__(self, bot, call) -> None:
        self.arg = None
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
            case 'lang':  # обработка работы с языком
                self._handle_lang()
            case 'main':  # обработка нажатий главного меню
                self._handle_menu()
            case 'field':  # обработка хода игрока
                self._handle_field()
            case 'choose_game_type':
                self._handle_choose_game_type()
            case 'ready':
                self._ready_to_play()
            case 'cancel_game':
                self._cancel_game()

    def _handle_lang(self):
        # УБРАТЬ ПОТОМ
        # self.db.clear_database()
        # 
        self.db.register_user(self.data, self.arg)
        self.bot.send_message(chat_id=self.data.from_user.id, text=self.get_str('successfully_registered', self.arg),
                              reply_markup=main_keyboard())

    def _handle_menu(self):
        match self.arg:
            case 'play':
                self.bot.send_message(chat_id=self.data.from_user.id, text=self.get_str('type_of_game', self.lang),
                                      reply_markup=choose_game_type())
            case 'play_with_bot':
                pass
            case 'stats':
                pass
            case 'rate':
                pass

    def _handle_field(self):
        # проверка на его ход
        this_user = self.db.find_user(self.data.from_user.id)
        game = self.db.find_game(this_user.game_id)

        if this_user.user_id == game.first_player_id and game.move_player is False:
            # не ход первого игрока
            self.bot.send_message(chat_id=this_user.user_id, text=f"Сейчас не ваш ход", reply_markup=gamefield())
            return

        elif this_user.user_id == game.second_player_id and game.move_player is True:
            # не ход второго игрока
            self.bot.send_message(chat_id=this_user.user_id, text=f"Сейчас не ваш ход", reply_markup=gamefield())
            return

        # проверка на занятость клетки
        gamefield_id_from_user = this_user.game_id
        if self.db.get_gamefield(gamefield_id_from_user, self.arg) is not 0:
            # клетка уже занята
            self.bot.send_message(chat_id=this_user.user_id, text=f"Эта клетка уже занята, выберите другую", reply_markup=gamefield())
            return

        # обработка хода
        gamefield_id_from_user = this_user.game_id
        gamefield_value = 1 if this_user.user_id == game.first_player_id else 2  # 1 - крестик, 2 - нолик
        self.db.edit_gamefield(gamefield_id_from_user, self.arg, gamefield_value)  

        self.db.update_move_player_status(game)

         # отправка сообщений об успешном ходе и переходе права хода к другому игроку
        if gamefield_value == 1:
            # ход крестика
            self.bot.send_message(chat_id=this_user.user_id, text=f"Вы сделали ход на {self.arg} клетку", reply_markup=None)
            
            # проверка на ничью
            if self.db.check_draw(gamefield_id_from_user) == True:
                self.bot.send_message(chat_id=this_user.user_id, text=f"Ничья", reply_markup=None)
                self.bot.send_message(chat_id=game.second_player_id, text=f"Ничья", reply_markup=None)

                self.db.finish_game(game.first_player_id,game.second_player_id,0)
                return

            # проверка на победу
            if self.db.check_win(gamefield_id_from_user,1) == True:
                self.bot.send_message(chat_id=this_user.user_id, text=f"Крестик победил!", reply_markup=None)
                self.bot.send_message(chat_id=game.second_player_id, text=f"Крестик победил!", reply_markup=None)

                self.db.finish_game(game.first_player_id,game.second_player_id,1)
                return

            self.bot.send_message(chat_id=game.second_player_id, text=f"Крестик походил, ваша очередь", reply_markup=gamefield())
            
            
        else:
            # ход нолика
            self.bot.send_message(chat_id=this_user.user_id, text=f"Вы сделали ход на {self.arg} клетку", reply_markup=None)
            
            # проверка на ничью
            if self.db.check_draw(gamefield_id_from_user) == True:
                self.bot.send_message(chat_id=this_user.user_id, text=f"Ничья", reply_markup=None)
                self.bot.send_message(chat_id=game.second_player_id, text=f"Ничья", reply_markup=None)

                self.db.finish_game(game.first_player_id,game.second_player_id,0)
                return

            # проверка на победу
            if self.db.check_win(gamefield_id_from_user,2) == True:
                self.bot.send_message(chat_id=this_user.user_id, text=f"Нолик победил!", reply_markup=None)
                self.bot.send_message(chat_id=game.first_player_id, text=f"Нолик победил!", reply_markup=None)

                self.db.finish_game(game.first_player_id,game.second_player_id,2)
                return

            self.bot.send_message(chat_id=game.first_player_id, text=f"Нолик походил, ваша очередь", reply_markup=gamefield())
                        

    def _handle_choose_game_type(self):
        match self.arg:
            case 'random':
                pass
            case 'find':
                text = f'Упомяни игрока, с которым хочешь поиграть\n\nНапример: ```@username```'
                msg = self.bot.send_message(chat_id=self.data.from_user.id, text=text, parse_mode='MarkdownV2',
                                            reply_markup=None)
                self.bot.register_next_step_handler(msg, self.play_register)

    def _cancel_game(self):
        this_user = self.db.find_user(self.data.from_user.id)

        players_id = self.db.cancel_game(this_user.game_id)

        for player_id in players_id:
            self.bot.send_message(chat_id=player_id, text=f"Предложение игры отклонено",
                                  reply_markup=main_keyboard())

    def _ready_to_play(self):
        match self.arg:
            case 'true':
                this_user = self.db.find_user(self.data.from_user.id)
                game = self.db.find_game(this_user.game_id)

                self.bot.send_message(chat_id=game.first_player_id, text=f"Вы крестик, ваш ход", reply_markup=gamefield())

                self.bot.send_message(chat_id=game.second_player_id, text=f"Вы нолик, ожидайте пока игрок сделает ход",
                                      reply_markup=None)

            case 'false':
                try:
                    this_user = self.db.find_user(self.data.from_user.id)
                    self.db.calc_game_result(this_user.user_id)
                    Logging().info(f'Игрок {this_user.username} отказался от игры №{this_user.game_id}')
                    players_id = self.db.cancel_game(this_user.game_id)

                    Logging().info(f'Игра №{this_user.game_id} была отменена')

                    for player_id in players_id:
                        self.bot.send_message(chat_id=player_id, text=f"Предложение игры отклонено",
                                              reply_markup=main_keyboard())
                except Exception as ex:
                    Logging().warning(f'Произошла ошибка: {str(ex)}')

    # !методы ниже нужно будет переорпеделить куда-то!

    # регистрация игры
    def play_register(self, message, finded_user=None):

        # илья тут для работы, например поиска игрока ты пишешь например
        # дописать еще чтобы по ссылке можно было типо t.me/tgjdfg

        throw_user = self.db.find_user(message.from_user.id)  # игрок кинувший инвайт
        find_user = self.db.find_user_by_tag(message.text)  # находим игрока

        if find_user is None:  # если он не найден
            self.bot.send_message(chat_id=message.from_user.id, text=f"{message.text} игрок не был найден.",
                                  reply_markup=main_keyboard())
            return

        find_game_id = find_user.game_id
        throw_game_id = throw_user.game_id

        null_game = -1

        if find_game_id == null_game and throw_game_id == null_game:
            self.bot.send_message(chat_id=message.from_user.id, text=f"Приглашение отправлено. Ожидаем ответа.",
                                  reply_markup=cancel_keyboard())
            self.bot.send_message(chat_id=find_user.user_id,
                                  text=f"{throw_user.username} пригласил вас сыграть вместе с ним.",
                                  reply_markup=ready_keyaboard())

            game = self.db.create_game(find_user.user_id, throw_user.user_id)

        else:  # такого не должно быть
            self.bot.send_message(chat_id=message.from_user.id, text=f"Кто-то из вас уже в игре\n(для выхода из неё напишите `/exit`)", parse_mode='markdown',
                                  reply_markup=main_keyboard())
            return

        # self.bot.send_message(chat_id=message.from_user.id, text=f"{message.text} Отправлено приглашение пользователю "+message.text, reply_markup=main_keyboard())

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
