from db import Database
from keyboards import main_keyboard, choose_game_type, ready_keyaboard, gamefield, cancel_keyboard
from language.langs import Language
from log import Logging

from TicTacToe.generate_gamefield import Generate_gamefield
from TicTacToe.keyboards import settings_keyboard, lang_keyboard


class Callback:
    def __init__(self, bot, call) -> None:
        self.arg = None
        self.data = call
        self.bot = bot
        self.db = Database()
        self.langs = Language()
        self.generate_gamefield = Generate_gamefield(self.db)
        self.lang = getattr(self.db.find_user(call.from_user.id), 'lang', 'en')

        self.get_str = self.langs.get_string_by_lang
        self.parse()

    def parse(self):
        command = self.data.data.split(':')[0]
        self.arg = self.data.data.split(':')[1]

        match command:
            case 'lang':  # обработка работы с языком
                self._handle_lang()
            case 'change_lang':
                self._handle_change_lang()
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
            case 'settings':
                self._handle_settings()

    def _handle_lang(self):
        self.db.register_user(self.data, self.arg)
        Logging.info(f'Зарегистрирован пользователь с id: {self.data.from_user.id}')
        self.bot.send_message(chat_id=self.data.from_user.id, text=self.get_str('successfully_registered', self.arg),
                              reply_markup=main_keyboard(self.data.from_user.id))

    def _handle_change_lang(self):
        self.db.change_lang(self.data.from_user.id, self.arg)
        user = self.db.find_user(self.data.from_user.id)
        Logging.info(f'Пользователь с id: {self.data.from_user.id} сменил язык на {self.arg}')
        self.bot.send_message(chat_id=self.data.from_user.id, text=self.get_str('lang_changed', user.lang),
                              reply_markup=main_keyboard(self.data.from_user.id))

    def _handle_menu(self):
        match self.arg:
            case 'play':
                self.bot.send_message(chat_id=self.data.from_user.id, text=self.get_str('type_of_game', self.lang),
                                      reply_markup=choose_game_type())
            case 'return_play':
                self.bot.send_message(chat_id=self.data.from_user.id, text=f"Продолжайте игру", reply_markup=gamefield())
            case 'cancel_game':
                this_user = self.db.find_user(self.data.from_user.id)
                self.give_up(this_user)

            case 'stats':
                this_user = self.db.find_user(self.data.from_user.id)
               
                self.bot.send_message(chat_id=self.data.from_user.id,
                 text="Статистика игрока @{username}\nUser id: {user_id}\nКоличество сыграных игр:  {games_count}\nКоличество выигранных игр: {wins_count}\nКоличество проигранных игр: {lose_count}\nРейтинг: {rating}".format(username=this_user.username, user_id=this_user.user_id, games_count=this_user.games_count, wins_count = this_user.wins_count,lose_count = this_user.lose_count,rating = this_user.rating ),
                                      reply_markup=main_keyboard(self.data.from_user.id))
            case 'rate':
                self.bot.send_message(chat_id=self.data.from_user.id, text="Ожидайте...",
                                      reply_markup=None)
                rating_list = self.db.calc_rating(self.data.from_user.id)
                message = 'Рейтинг'
                for index, player in enumerate(rating_list):
                    if player.user_id == self.data.from_user.id:
                        rating_for_outputng = player.rating
                        place_in_the_rating = index+1

                    if index <= 10:
                        message +="\n{count_of_player}. @{username} — {rating}".format(count_of_player = index+1, username = player.username, rating = player.rating)
                
                message +="\n..."
                                      
                message += "\nВы на {place} месте, ваш рейтинг: {rating_out}".format(place = place_in_the_rating,rating_out = rating_for_outputng)
                self.bot.send_message(chat_id=self.data.from_user.id, text=message,
                                      reply_markup=main_keyboard(self.data.from_user.id))

            case 'settings':
                text = 'Настройки'
                self.bot.send_message(chat_id=self.data.from_user.id, text=text,
                              reply_markup=settings_keyboard())
                        

    def _handle_field(self):
        this_user = self.db.find_user(self.data.from_user.id)
        Logging.info(f'Игрок {this_user.username} делает ход в игре №{this_user.game_id}')
        game = self.db.find_game(this_user.game_id)

        # сдаться
        if self.arg == 'leave':
            self.give_up(this_user)
            return

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
        if self.db.get_gamefield(gamefield_id_from_user, self.arg) != 0:
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
            self.bot.send_message(chat_id=this_user.user_id,
                                  text=self.generate_gamefield.get_gamefield(game.gamefield_id),
                                  reply_markup=gamefield())
            
            # проверка на ничью
            if self.db.check_draw(gamefield_id_from_user) == True:
                self.bot.send_message(chat_id=this_user.user_id, text=f"Ничья", reply_markup=None)
                self.bot.send_message(chat_id=game.second_player_id, text=f"Ничья", reply_markup=None)

                self.db.finish_game(game.first_player_id, game.second_player_id, 0)
                self.stats_after_game(this_user.user_id, game.second_player_id, 0)
                return

            # проверка на победу
            if self.db.check_win(gamefield_id_from_user,1) == True:
                self.bot.send_message(chat_id=this_user.user_id, text=f"Крестик победил!", reply_markup=None)
                self.bot.send_message(chat_id=game.second_player_id, text=f"Крестик победил!", reply_markup=None)

                self.db.finish_game(game.first_player_id, game.second_player_id, 1)
                self.stats_after_game(game.first_player_id, game.second_player_id)
                Logging.info(f'Игра №{game.id} завершилась')
                return

            self.bot.send_message(chat_id=game.second_player_id, text=f"Крестик походил, ваша очередь", reply_markup=None)
            self.bot.send_message(chat_id=game.second_player_id, text=self.generate_gamefield.get_gamefield(game.gamefield_id),
                                  reply_markup=gamefield())
            
        else:
            # ход нолика
            self.bot.send_message(chat_id=this_user.user_id, text=f"Вы сделали ход на {self.arg} клетку", reply_markup=None)
            self.bot.send_message(chat_id=this_user.user_id,
                                  text=self.generate_gamefield.get_gamefield(game.gamefield_id),
                                  reply_markup=gamefield())
            
            # проверка на ничью
            if self.db.check_draw(gamefield_id_from_user) == True:
                self.bot.send_message(chat_id=this_user.user_id, text=f"Ничья", reply_markup=None)
                self.bot.send_message(chat_id=game.second_player_id, text=f"Ничья", reply_markup=None)

                self.db.finish_game(game.first_player_id,game.second_player_id,0)
                self.stats_after_game(this_user.user_id, game.second_player_id, 0)
                Logging.info(f'Игра №{game.id} завершилась')
                return

            # проверка на победу
            if self.db.check_win(gamefield_id_from_user,2) == True:
                self.bot.send_message(chat_id=this_user.user_id, text=f"Нолик победил!", reply_markup=None)
                self.bot.send_message(chat_id=game.first_player_id, text=f"Нолик победил!", reply_markup=None)

                self.db.finish_game(game.first_player_id,game.second_player_id,2)
                self.stats_after_game(game.second_player_id, game.first_player_id)
                Logging.info(f'Игра №{game.id} завершилась')
                return

            self.bot.send_message(chat_id=game.first_player_id, text=f"Нолик походил, ваша очередь", reply_markup=None)
            self.bot.send_message(chat_id=game.first_player_id,
                                  text=self.generate_gamefield.get_gamefield(game.gamefield_id),
                                  reply_markup=gamefield())
                        

    def _handle_choose_game_type(self):
        match self.arg:
            case 'random':
                find_user = self.db.find_user(self.data.from_user.id)
                while True:
                    random_user = self.db.get_random_user()
                    if random_user.user_id != find_user.user_id:
                        break

                find_game_id = find_user.game_id
                random_game_id = random_user.game_id

                null_game = -1

                if find_game_id == null_game and random_game_id == null_game:
                    self.bot.send_message(chat_id=find_user.user_id, text=f"Приглашение отправлено игроку {random_user.username}. Ожидаем ответа.",
                                          reply_markup=cancel_keyboard())
                    self.bot.send_message(chat_id=random_user.user_id,
                                          text=f"{find_user.username} пригласил вас сыграть вместе с ним.",
                                          reply_markup=ready_keyaboard())

                    game = self.db.create_game(find_user.user_id, random_user.user_id)

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
                                  reply_markup=main_keyboard(player_id))

    def _ready_to_play(self):
        match self.arg:
            case 'true':
                this_user = self.db.find_user(self.data.from_user.id)
                game = self.db.find_game(this_user.game_id)

                Logging.info(f'Игра №{game.id} началась')

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
                                              reply_markup=main_keyboard(player_id))
                except Exception as ex:
                    Logging().warn(f'Произошла ошибка: {str(ex)}')

    # регистрация игры
    def play_register(self, message, finded_user=None):
        throw_user = self.db.find_user(message.from_user.id)  # игрок кинувший инвайт
        find_user = self.db.find_user_by_tag(message.text)  # находим игрока

        if find_user is None:  # если он не найден
            # поиск игрока по ссылке
            find_user = self.db.find_user_by_url(message.text)
            if find_user is None:
                self.bot.send_message(chat_id=message.from_user.id, text=f"{message.text} игрок не был найден.",
                                    reply_markup=main_keyboard(message.from_user.id))
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
            self.bot.send_message(chat_id=message.from_user.id, text=f"Кто-то из вас уже в игре\n(для выхода из неё напишите `/cancel_game`)", parse_mode='markdown',
                                  reply_markup=main_keyboard(message.from_user.id))
            return

    def give_up(self, this_user):
        self.db.calc_game_result(this_user.user_id)
        Logging().info(f'Игрок {this_user.username} сдался в игре №{this_user.game_id}')
        players_id = self.db.cancel_game(this_user.game_id)

        self.bot.send_message(chat_id=this_user.user_id, text=f"Вы успешно сдались",
                              reply_markup=None)

        for player_id in players_id:
            if player_id != this_user.user_id:
                self.bot.send_message(chat_id=player_id, text=f"Ваш соперник сдался",
                                      reply_markup=None)
                self.stats_after_game(player_id, this_user.user_id)

    def stats_after_game(self, winner_id, loser_id, val=1):
        winner = self.db.find_user(winner_id)
        winner_text = f'Ваша статистика изменилась после игры: \n🔺 Рейтинг: {winner.rating} (+10)\n🔺 Игр: {winner.games_count} (+1)\n🔺Побед: {winner.wins_count} (+1)'
        loser = self.db.find_user(loser_id)
        loser_text = f'Ваша статистика изменилась после игры: \n🔻 Рейтинг: {loser.rating} (-10)\n🔺 Игр: {loser.games_count} (+1)\n🔺Поражений: {loser.lose_count} (+1)'

        if val == 0:
            winner_text = f'Ваша статистика не изменилась после игры: \n♦️ Рейтинг: {winner.rating}\n♦️ Игр: {winner.games_count}\n♦️Побед: {winner.wins_count}'
            loser_text = f'Ваша статистика не изменилась после игры: \n♦️ Рейтинг: {winner.rating}\n♦️ Игр: {winner.games_count}\n♦️Побед: {winner.wins_count}'

        self.bot.send_message(chat_id=winner_id, text=winner_text,
                              reply_markup=main_keyboard(winner.user_id))
        self.bot.send_message(chat_id=loser_id, text=loser_text,
                              reply_markup=main_keyboard(loser.user_id))

    def _handle_settings(self):
        match self.arg:
            case 'change_lang':
                self.bot.send_message(chat_id=self.data.from_user.id, text='Выберите язык для смены из доступных: ',
                    reply_markup=lang_keyboard(1))
            case 'reset_stats':
                self.db.reset_stats(self.data.from_user.id)
                self.bot.send_message(chat_id=self.data.from_user.id, text='Вы успешно сбросили статистику профиля',
                              reply_markup=main_keyboard(self.data.from_user.id))
            case 'back':
                self.bot.send_message(chat_id=self.data.from_user.id, text='Вы вернулись назад',
                                      reply_markup=main_keyboard(self.data.from_user.id))