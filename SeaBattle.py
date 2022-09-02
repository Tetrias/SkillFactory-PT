# Игра "Морской бой"
# Не закончено.
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
    for x in range(board_size):
        for y in range(board_size):
            row.append(x)
            col.append(y)
            moves = list(product(row, col))
    return list(set(moves))


def contour(x_y, rotate=False):
    res = []
    if not x_y:
        return False
    row, col = x_y[0], x_y[1]
    if rotate:
        near = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    else:
        near = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
    for x, y in near:
        if 0 > (x + row) or (x + row) >= board_size or 0 > (y + col) or (y + col) >= board_size:
            continue
        else:
            res += [(x + row, y + col)]
    return res


def clean_contour(available_move, cont):
    for i in available_move[:]:
        if i in cont:
            available_move.remove(i)
            cont.remove(i)
    return available_move


def get_board():
    field = [[empty_cell for _ in range(board_size)] for _ in range(board_size)]
    return field


def draw_board(field, AI=True):
    field_res = ''
    field_res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
    for i, row in enumerate(field):
        field_res += f"\n{i + 1} | " + " | ".join(row) + " |"
    if AI:
        field_res = field_res.replace(ship_cell, empty_cell)
    return field_res


def cycle_for_getting_board():
    field = get_board()
    while True:
        r = random_ship(field)
        if r:
            return r


def get_free_space(length, moves, ship):
    if not ship:
        return moves
    elif length > 1:
        first_coord = ship[0]
        result = contour(first_coord)
        moves = clean_contour(moves, result)
        second_coord = ship[1]
        result = contour(second_coord)
        moves = clean_contour(moves, result)
        if length == 3:
            third_coord = ship[2]
            result = contour(third_coord)
            moves = clean_contour(moves, result)
    else:
        result = contour(ship)
        moves = clean_contour(moves, result)
    return moves


def place_ship_on_board(ships, board):
    for i in range(len(ships)):
        for x, y in ships:
            board[x][y] = ship_cell


def random_ship(board):
    moves = all_moves()
    counter = 0
    for i in ship_size:
        ship = []
        while True:
            counter += 1
            if counter > 2000:
                return False
            try:
                cell = choice(moves)
            except IndexError:
                return False
            if board[cell[0]][cell[1]] == empty_cell:
                if i == 1:
                    ship = cell
                    board[cell[0]][cell[1]] = ship_cell
                    moves = get_free_space(i, moves, ship)
                    break
                else:
                    rotation = rotate_ship(i, board, cell)
                    if rotation:
                        ship = rotation
                        place_ship_on_board(rotation, board)
                        moves = get_free_space(i, moves, ship)
                        break
    return board


def rotate_ship(s_ship, board, cell):
    cont = contour(cell, True)
    rot_cell = []
    for i in cont:
        a = []
        if board[int(i[0])][int(i[1])] == empty_cell:
            if s_ship == 2:
                rot_cell.append(cell)
                rot_cell.append(i)
                return rot_cell
            else:
                a = (i[0] - cell[0], i[1] - cell[1])
                a = (a[0] + i[0], a[1] + i[1])
                if 0 > a[0] or a[0] >= board_size or 0 > a[1] or a[1] >= board_size:
                    continue
                elif board[a[0]][a[1]] == empty_cell:
                    rot_cell.append(cell)
                    rot_cell.append(i)
                    rot_cell.append(a)
                    return rot_cell


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
    field = player_1
    ai_field = player_2
    print(draw_board(field, False))
    print()
    print(draw_board(ai_field))


board_size = 6
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
