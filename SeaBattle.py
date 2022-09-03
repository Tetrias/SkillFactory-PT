# Игра "Морской бой"
# Не закончено.
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
        return "Вы уже совершали ход в эту."


class LengthOutException(BoardException):
    def __str__(self):
        return "Цифр меньше чем необходимых для хода."


class DigitsException(BoardException):
    def __str__(self):
        return "Вводить необходимо цифры."


# Класс для проверки корректности хода игрока.
class CheckMove:
    def __init__(self, user_input, field):
        self.x = user_input[0:1]
        self.y = user_input[1:2]
        self.r = user_input[2:3]
        self.length = len(user_input)
        self.r_digits = (2, 4, 6, 8)
        self.field = field

    # Проверяем всевозможные варианты некорректного ввода и отлавливаем соответсвующее им исключение.
    def check_exception(self):
        try:
            if self.length < 2:
                raise LengthOutException
            elif not self.x.isdigit() or not self.y.isdigit():
                raise DigitsException
            elif int(self.x) <= 0 or int(self.x) <= 0 or int(self.x) > 6 or int(self.x) > 6:
                raise BoardOutException
            elif self.field[int(self.x) - 1][int(self.y) - 1] == damaged_ship or \
                    self.field[int(self.x) - 1][int(self.y) - 1] == destroyed_ship:
                raise BoardUsedException
        except BoardException as er:
            print(er)
        else:
            return True


# Функция для получения всевозможных ходов.
def all_moves():
    row, col, moves = [], [], []
    for x in range(board_size):
        for y in range(board_size):
            row.append(x)
            col.append(y)
            moves = list(product(row, col))
    return list(set(moves))


# Функция для определения контуров хода.
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


# Функция удаляющая из возможных ходов те, совершать которые нет смысла.
def clean_contour(available_move, cont):
    for i in available_move[:]:
        if i in cont:
            available_move.remove(i)
            cont.remove(i)
    return available_move


# Функция для получения доски.
def get_board():
    board = [[empty_cell for _ in range(board_size)] for _ in range(board_size)]
    return board


# Функция для рисования доски.
def draw_board(board, AI=True):
    field_res = ''
    field_res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
    for i, row in enumerate(board):
        field_res += f"\n{i + 1} | " + " | ".join(row) + " |"
    if AI:
        field_res = field_res.replace(ship_cell, empty_cell)
    return field_res


# Функция вызывающая цикл, который повторяется до тех пор, пока корабли не будут расставлены.
def cycle_for_getting_board():
    while True:
        board = get_board()
        board = random_ship(board)
        if board:
            if correct_board(board):
                return board


# Функция для проверки корректности расстановки кораблей.
def correct_board(board):
    row_found, colum_found = 0, 0
    N = len(board[0])
    for elem in board:
        colum_found = 0
        for row in range(N - 1):
            if elem[row] == ship_cell and elem[row + 1] == ship_cell:
                row_found += 1
    for x in range(0, N - 1):
        for y in range(0, N - 1):
            if board[x][y] == ship_cell and board[x][y + 1] == ship_cell:
                colum_found += 1
    for i in range(1, N - 1):
        for j in range(1, N - 1):
            if board[i][j] == ship_cell:
                if board[i + 1][j + 1] == ship_cell:
                    return False
                if board[i + 1][j - 1] == ship_cell:
                    return False
                if board[i - 1][j - 1] == ship_cell:
                    return False
                if board[i - 1][j + 1] == ship_cell:
                    return False
    if row_found >= 4 or colum_found >= 4:
        return False
    else:
        return True


# Функция для удаления клеток из случайного выбора расстановки кораблей.
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


# Функция для замены пустых клеток на клетки корабля.
def place_ship_on_board(ships, board):
    for i in range(len(ships)):
        for x, y in ships:
            board[x][y] = ship_cell


# Основная функция для получения координат корабля.
def random_ship(board):
    moves = all_moves()
    counter = 0
    for i in ship_pool:
        while True:
            counter += 1
            if counter > 2000:
                return None
            try:
                cell = choice(moves)
            except IndexError:
                return None
            if board[cell[0]][cell[1]] == empty_cell:
                if i == 1:
                    board[cell[0]][cell[1]] = ship_cell
                    moves = get_free_space(i, moves, cell)
                    break
                else:
                    rotation = rotate_ship(i, board, cell)
                    if rotation:
                        place_ship_on_board(rotation, board)
                        moves = get_free_space(i, moves, rotation)
                        break
    return board


# Функция для выбора направления корабля.
def rotate_ship(s_ship, board, cell):
    cont = contour(cell, True)
    rot_cell = []
    for i in cont:
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


# Функция для получения хода.
def get_input(available_move, player, field):
    if player == 'Человек':
        print('Сделайте ход.')
        print('Подсказка: нужно ввести два числа, где первое - ряд, второе - столбец.')
        print('Или введите "выход" для завершения игры.')
        while True:
            user_input = input('>>> ').replace(" ", "")
            # Отправляем в класс проверки ходов, если метод проверки не вернул True, повторить цикл.
            if user_input == "выход":
                print('Благодарим за игру!')
                exit()
            check_input = CheckMove(user_input, field)
            valid_input = check_input.check_exception()
            if valid_input is True:
                x, y = int(user_input[0]) - 1, int(user_input[1]) - 1
                break
    else:
        ai_input = choice(available_move)
        x, y = ai_input[0], ai_input[1]
    return x, y


# Функция ИИ удаляющая ненужные ходы из возможных.
def ai_logic(available_move, ai_input):
    res = contour(ai_input)
    available_move = clean_contour(available_move, res)
    return available_move


def ships_left(target):
    ship_found = 0
    for row in target:
        for elem in range(0, board_size - 1):
            if row[elem] == ship_cell:
                ship_found += 1
    return ship_found


# Функция для определения попаданий.
def shoot(available_move, turn, target):
    x, y = get_input(available_move, turn, target)
    if target[x][y] == empty_cell or target[x][y] == miss_cell or target[x][y] == damaged_ship:
        target[x][y] = miss_cell
        return 'miss'
    elif target[x][y] == ship_cell:
        cont = contour([x, y], True)
        ships = None
        for s_x, s_y in cont:
            if target[s_x][s_y] == ship_cell:
                target[x][y] = damaged_ship
                return 'get'
            elif target[s_x][s_y] == damaged_ship or target[s_x][s_y] == destroyed_ship:
                elem = ((s_x - x), (s_y - y))
                elem = (elem[0] + s_x, elem[1] + s_y)
                if 0 < elem[0] or elem[0] < board_size or 0 < elem[1] or elem[1] < board_size:
                    if target[elem[0]][elem[1]] == ship_cell:
                        target[x][y] = destroyed_ship
                        if turn == 'Человек':
                            ships = ships_left(target)
                        else:
                            ai_logic(available_move, (x, y))
                            ships = ships_left(target)
                    else:
                        target[x][y] = damaged_ship
                        return 'get'
            else:
                target[x][y] = destroyed_ship
                ships = ships_left(target)
                break
        return ships


# Основная функция игры.
def play_game():
    user, ai = cycle_for_getting_board(), cycle_for_getting_board()
    current_player, next_player = ('Человек1', user), ('Компьютер', ai)
    available_move = all_moves()
    while True:
        print(f'{draw_board(user, False)}\n  ' + '+' * 25 + f'\n{draw_board(ai)}')
        result = shoot(available_move, current_player[0], next_player[1])
        if result == 'miss':
            print('Промах!')
            next_player, current_player = current_player, next_player
            continue
        elif result == 'get':
            print('Попал!')
            continue
        elif result == 'kill' or int:
            print('Убил!')
            if result == 0:
                return current_player[0]
            else:
                continue


board_size = 6
ship_pool = [3, 2, 2, 1, 1, 1, 1]
empty_cell = '0'
ship_cell = '■'
destroyed_ship = 'X'
damaged_ship = '□'
miss_cell = '•'
print('Добро пожаловать в игру "Морской бой"')
print('Подождите пока корабли встанут по местам.')

# Основной код, в виде цикла, для возможности повтора игры.
while True:
    winner = play_game()
    print(f'{winner} победил!')
    print('Хотите сыграть ещё раз (да для повтора)?')
    input().lower()
    if not input().lower() == 'да':
        print('Благодарим за игру!')
        exit()
