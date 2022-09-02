# Игра "Морской бой"
# В процессе написания.
from sys import exit
from itertools import product
from random import randint


# Классы исключений, для отлова и отображения сообщений пользователю.
class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Нельзя делать ход за пределы доски."


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже совершали ход в эту клетку или она находиться рядом с кораблем."


class LengthOutException(BoardException):
    def __str__(self):
        return "Символов меньше чем необходимых для хода."


class DigitsException(BoardException):
    def __str__(self):
        return "Вводить необходимо цифры."


class IncorrectLettersInChoice(BoardException):
    def __str__(self):
        return 'Необходимо указать одну из цифр: "4" - влево, "6" - вправо, 2 - вниз или 8 - вверх.'


# Класс для проверки корректности хода игрока.
class CheckMove:
    def __init__(self, user_input, *args):
        self.x = user_input[0:1]
        self.y = user_input[1:2]
        self.r = user_input[2:3]
        self.length = len(user_input)
        self.args = args
        self.r_digits = (2, 4, 6, 8)

    # Проверяем всевозможные варианты некорректного ввода и отлавливаем соответсвующее им исключение.
    def check_exception(self):
        try:
            if self.length < 2:
                raise LengthOutException
            elif not self.x.isdigit() and not self.y.isdigit():
                raise DigitsException
            elif True in self.args:
                if self.length < 3:
                    raise LengthOutException
                elif not self.r.isdigit():
                    raise DigitsException
                elif int(self.r) not in self.r_digits:
                    raise IncorrectLettersInChoice
            elif int(self.x) not in range(1, 6 + 1) and not int(self.y) in range(1, 6 + 1):
                raise BoardOutException
        except BoardException as er:
            print(er)
        else:
            return True


# Класс для хранения объектов рисования доски.
class Dots:
    empty_cell = '0'
    ship_cell = '■'
    destroyed_ship = 'X'
    damaged_ship = '□'
    miss_cell = '•'
    field_size = 6


# Класс для логики игры.
class Game:
    field_size = 6
    ships_size = [3, 2, 2, 1, 1, 1, 1]


# Класс для отрисовки поля и изменения в нем.
class Field:
    def __init__(self):
        self.size = Game.field_size
        self.board = [[Dots.empty_cell for _ in range(self.size)] for _ in range(self.size)]

    @property
    def all_moves(self):
        row, col = [], []
        for x in range(self.size):
            for y in range(self.size):
                row.append(x)
                col.append(y)
        return list(product(row, col))

    def __str__(self):
        board_res = ''
        board_res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.board):
            board_res += f"\n{i + 1} | " + " | ".join(row) + " |"
        if current_player != 'Человек':
            board_res = board_res.replace(Dots.ship_cell, Dots.empty_cell)
        return board_res


# Класс для взаимодействия с кораблями.
class Ship:
    pass


# Класс для логики игроков.
class Player:
    pass


# Класс для пользователя.
class User(Player):
    pass


# Класс для ИИ.
class AI(Player):
    pass


def play_game():
    pass


while True:
    break
