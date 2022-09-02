# Игра "Морской бой"
# Не законченно.
from sys import exit
from itertools import product
from random import choice


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
        return "Цифр меньше чем необходимых для хода."


class DigitsException(BoardException):
    def __str__(self):
        return "Вводить необходимо цифры."


# Класс для проверки корректности хода игрока.
class CheckMove:
    def __init__(self, user_input):
        self.x = user_input[0:1]
        self.y = user_input[1:2]
        self.r = user_input[2:3]
        self.length = len(user_input)
        self.r_digits = (2, 4, 6, 8)

    # Проверяем всевозможные варианты некорректного ввода и отлавливаем соответсвующее им исключение.
    def check_exception(self):
        try:
            if self.length < 2:
                raise LengthOutException
            elif not self.x.isdigit() and not self.y.isdigit():
                raise DigitsException
            elif int(self.x) <= 0 or int(self.x) <= 0 or int(self.x) > 6 or int(self.x) > 6:
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


# Класс для отрисовки поля и изменения в нем.
class Field:
    def __init__(self):
        self.size = Game.field_size
        self.board = [[Dots.empty_cell for _ in range(self.size)] for _ in range(self.size)]

    @property
    def all_moves(self):
        row, col, moves = [], [], []
        for x in range(self.size):
            for y in range(self.size):
                row.append(x)
                col.append(y)
                moves = list(product(row, col))
        return list(set(moves))

    def __str__(self):
        board_res = ''
        board_res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.board):
            board_res += f"\n{i + 1} | " + " | ".join(row) + " |"
        # if current_player != 'Человек':
        #     board_res = board_res.replace(Dots.ship_cell, Dots.empty_cell)
        # return board_res


# Класс для взаимодействия с кораблями.
class Ship:
    pass


# Класс для логики игроков.
class Player:
    def __init__(self):
        self.player = "" #'Человек'
        self.available_move = Field().all_moves

    def get_input(self):
        if self.player == 'Человек':
            print('Сделайте ход.')
            print('Подсказка: нужно ввести два числа, где первое - ряд, второе - столбец.')
            print('Или введите "выход" для завершения игры.')
            got_move = User().get_shot_input()
            x, y = int(got_move[0]) - 1, int(got_move[1]) - 1
        else:
            got_move = AI().get_ai_move()
            x, y = got_move[0], got_move[1]
        return x, y


# Класс для пользователя.
class User(Player):
    # Получаем ход игрока и проверяем корректность ввода.
    @staticmethod
    def get_shot_input():
        while True:
            user_input = input().replace(" ", "")
            # Отправляем в класс проверки ходов, если метод проверки не вернул True, повторить цикл.
            check_input = CheckMove(user_input)
            valid_input = check_input.check_exception()
            if valid_input is True:
                return user_input


# Класс для ИИ.
class AI(Player):
    # Получаем ход компьютера.

    def get_ai_move(self):
        ai_input = choice(self.available_move)
        return ai_input

    # Обрисовываем контур, если предыдущий ход попал или убил корабль.
    @staticmethod
    def contour(x_y):
        res = []
        row, col = x_y[0], x_y[1]
        near = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
        for x, y in near:
            res += [(x + row, y + col)]
        return res

    # Убираем клетки в которые ходить уже не нужно.
    @staticmethod
    def clean_contour(coord, cont):
        for i in coord[:]:
            if i in cont:
                coord.remove(i)
                cont.remove(i)
        return coord


# Класс для логики.
class Game:
    field_size = 6
    ships_size = [3, 2, 2, 1, 1, 1, 1]


while True:
    g = Game()
    a = Player().get_input()
    print(a)
    break
