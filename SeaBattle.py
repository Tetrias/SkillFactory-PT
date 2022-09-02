# Игра "Морской бой"
# Не законченно.
from sys import exit
from itertools import product
from random import choice
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
        self.moves = all_moves()

    # Проверяем всевозможные варианты некорректного ввода и отлавливаем соответсвующее им исключение.
    def check_exception(self):
        try:
            if self.length < 2:
                raise LengthOutException
            elif not self.x.isdigit() and not self.y.isdigit():
                raise DigitsException
            elif int(self.x) <= 0 or int(self.x) <= 0 or int(self.x) > 6 or int(self.x) > 6:
                raise BoardOutException
            elif (int(self.x), int(self.y)) not in self.moves:
                raise BoardUsedException
        except BoardException as er:
            print(er)
        else:
            return True


def all_moves():
    row, col, moves = [], [], []
    for x in range(field_size):
        for y in range(field_size):
            row.append(x)
            col.append(y)
            moves = list(product(row, col))
    return list(set(moves))


def get_field():
    field = [[empty_cell for _ in range(field_size)] for _ in range(field_size)]
    return field


def draw_field(field, player):
    field_res = ''
    field_res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
    for i, row in enumerate(field):
        field_res += f"\n{i + 1} | " + " | ".join(row) + " |"
    if player:
        field_res = field_res.replace(ship_cell, empty_cell)
    return field_res


def cycle_for_getting_board():
    field = get_field()
    while True:
        r = random_ship(field)
        if r:
            return field, r


def is_space_free():
    pass


def random_ship(board):
    moves = all_moves()
    counter = 0
    ships = []
    for i in ship_size:
        while True:
            counter += 1
            if counter > 2000:
                return False
            cell = choice(moves)
            if board[cell[0]][cell[1]] == '0':
                if i == 1:
                    ships.append(cell)
                    break
                else:
                    rotation = rotate_ship(i, board, cell)
                    if rotation:
                        ships.append(rotation)
                        break
    return ships


def rotate_ship(s_ship, board, cell):
    cont = contour(cell, True)
    rot_cell = []
    for i in cont:
        a = []
        if board[int(i[0])][int(i[1])] == '0':
            if s_ship == 2:
                rot_cell.append(cell)
                rot_cell.append(i)
                return rot_cell
            else:
                a = (i[0] - cell[0], i[1] - cell[1])
                a = (a[0] + i[0], a[1] + i[1])
                if 0 > a[0] or a[0] >= field_size or 0 > a[1] or a[1] >= field_size:
                    continue
                elif board[a[0]][a[1]] == '0':
                    print(a[0], a[1])
                    rot_cell.append(cell)
                    rot_cell.append(i)
                    rot_cell.append(a)
                    return rot_cell


def contour(x_y, rotate=False):
    moves = all_moves()
    res = []
    row, col = x_y[0], x_y[1]
    if rotate:
        near = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    else:
        near = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
    for x, y in near:
        if 0 > (x + row) or (x + row) >= field_size or 0 > (y + col) or (y + col) >= field_size:
            continue
        else:
            res += [(x + row, y + col)]
    return res


def clean_contour(available_move, cont):
    for i in available_move[:]:
        if i in cont:
            available_move.remove(i)
            cont.remove(i)
    return cont


def get_input(player, available_move):
    if player == 'Человек':
        print('Сделайте ход.')
        print('Подсказка: нужно ввести два числа, где первое - ряд, второе - столбец.')
        print('Или введите "выход" для завершения игры.')
        while True:
            user_input = input().replace(" ", "")
            # Отправляем в класс проверки ходов, если метод проверки не вернул True, повторить цикл.
            check_input = CheckMove(user_input)
            valid_input = check_input.check_exception()
            if valid_input is True:
                x, y = int(user_input[0]) - 1, int(user_input[1]) - 1
                break
    else:
        ai_input = choice(available_move)
        x, y = ai_input[0], ai_input[1]
    return x, y


def play_game():
    player_1 = cycle_for_getting_board()
    player_2 = cycle_for_getting_board()
    field = player_1[0]
    ships = player_1[1]
    print(player_1[1])


field_size = 6
ship_size = [3, 2, 2, 1, 1, 1, 1]
empty_cell = '0'
ship_cell = '■'
destroyed_ship = 'X'
damaged_ship = '□'
miss_cell = '•'
print('Добро пожаловать в игру "Морской бой"')
print('Подождите пока корабли встанут по местам.')

while True:
    play_game()
    break
