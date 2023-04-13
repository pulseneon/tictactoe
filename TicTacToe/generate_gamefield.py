# get_gamefield_obj
from TicTacToe.db import Database


def return_field(value):
    # 0 - пусто, 1 - крестик, 2 - нолик
    if value == 0:
        return '⬜️'
    if value == 1:
        return '❎'
    if value == 2:
        return '🅾️'


class Generate_gamefield():

    def __init__(self, db):
        self.db = db

    def get_gamefield(self, gamefield_id) -> str:
        field = ''
        gamefield = self.db.get_gamefield_obj(gamefield_id)

        field += '-' * 22 + '\n'
        field += '|'
        field += return_field(gamefield.field1)
        field += '|'
        field += return_field(gamefield.field2)
        field += '|'
        field += return_field(gamefield.field3)
        field += '|' + '\n'
        field += '-'* 22 + '\n'
        field += '|'
        field += return_field(gamefield.field4)
        field += '|'
        field += return_field(gamefield.field5)
        field += '|'
        field += return_field(gamefield.field6)
        field += '|' + '\n'
        field += '-' * 22 + '\n'
        field += '|'
        field += return_field(gamefield.field7)
        field += '|'
        field += return_field(gamefield.field8)
        field += '|'
        field += return_field(gamefield.field9)
        field += '|'+ '\n'
        field += '-' * 22

        return field
