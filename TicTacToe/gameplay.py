from operator import truediv
import telebot
import emoji
from telebot import types

game_board = [" "] * 9
current_player = "❌"
current_playerID = None
playerX = None
playerO = None


def check_win(board):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]

    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] != " ":
            return board[condition[0]]

    if " " not in board:
        return "Draw"

    return None

def display_board(board):
    row1 = "|".join(board[0:3])
    row2 = "|".join(board[3:6])
    row3 = "|".join(board[6:9])

    board = f"""------------------
| {row1}|
------------------
| {row2}|
------------------
| {row3}|
------------------"""
    return board

@bot.message_handler(func=lambda message: message.text in ['1', '2', '3', '4', '5', '6', '7', '8', '9'] and (message.chat.id == playerX or message.chat.id == playerO))
def tic_tac_toe(message):

    global current_player
    global current_playerID
    global game_board
    global playerX
    global playerO

    if(message.chat.id == playerX):
        bPlayerX = True

if (message.chat.id == playerX and bPlayerX == True):
        
        if playerO == None:
            bot.send_message(chat_id=message.chat.id, text="Please wait for another player to join.")
        elif game_board[int(message.text) - 1] == " ":
            game_board[int(message.text) - 1] = current_player
            result = check_win(game_board)
            if result:
                bot.send_message(chat_id=playerX, text=display_board(game_board))
                bot.send_message(chat_id=playerO, text=display_board(game_board))
                bot.send_message(chat_id=playerX, text=f"{result} wins!\nThanks for playing.")
                bot.send_message(chat_id=playerO, text=f"{result} wins!\nThanks for playing.")
                game_board = [" "] * 9
                playerX = None
                playerO = None
                current_player = "❌"
            else:
                bot.send_message(chat_id=playerX, text=display_board(game_board))
                bot.send_message(chat_id=playerO, text=display_board(game_board))
                if current_player == "❌" :
                    current_player = "⭕️"
                    bot.send_message(chat_id=playerO, text="It's your turn!", reply_markup=markup)
                else:
                    current_player = "❌"
                    bot.send_message(chat_id=playerX, text="It's your turn!", reply_markup=markup)
        else:
            bot.send_message(chat_id=message.chat.id, text="This position is already taken. Please try again.")
        
    else:
        if playerX == None:
            bot.send_message(chat_id=message.chat.id, text="Please wait for another player to join.")
        elif game_board[int(message.text) - 1] == " ":
            game_board[int(message.text) - 1] = current_player
            result = check_win(game_board)
            if result:
                bot.send_message(chat_id=playerX, text=display_board(game_board))
                bot.send_message(chat_id=playerO, text=display_board(game_board))
                bot.send_message(chat_id=playerX, text=f"{result} wins!\nThanks for playing.")
                bot.send_message(chat_id=playerO, text=f"{result} wins!\nThanks for playing.")
                game_board = [" "] * 9
                playerX = None
                playerO = None
                current_player = "❌"
            else:
                bot.send_message(chat_id=playerX, text=display_board(game_board))
                bot.send_message(chat_id=playerO, text=display_board(game_board))
                if current_player == "❌" :
                    current_player = "⭕️"
                    bot.send_message(chat_id=playerO, text="It's your turn!", reply_markup=markup)
                else:
                    current_player = "❌"
                    bot.send_message(chat_id=playerX, text="It's your turn!", reply_markup=markup)
        else:
            bot.send_message(chat_id=message.chat.id, text="This position is already taken. Please try again.")       
    bPlayerX = False        

if name == "main":
    bot.polling()