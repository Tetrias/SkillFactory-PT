# Игра "Морской бой"
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
    def __init__(self, user_input, board):
        self.x = user_input[0:1]
        self.y = user_input[1:2]
        self.length = len(user_input)
        self.board = board

    # Проверяем всевозможные варианты некорректного ввода и отлавливаем соответсвующее им исключение.
    def check_exception(self):
        g = Game()
        try:
            # Если вводимых игроком символов меньше двух.
            if self.length < 2:
                raise LengthOutException
            # Если вводимые игроком символы не являются числом.
            elif not self.x.isdigit() or not self.y.isdigit():
                raise DigitsException
            # Если числа не в пределах 1-6.
            elif int(self.x) <= 0 or int(self.y) <= 0 or int(self.x) > g.board_size or int(self.y) > g.board_size:
                raise BoardOutException
            # Если координаты указывают на клетку не соответствующую ходу.
            elif self.board[int(self.x) - 1][int(self.y) - 1] != Game().empty_cell and \
                    self.board[int(self.x) - 1][int(self.y) - 1] != Game().ship_cell:
                raise BoardUsedException
        # Вывести соответствующее сообщение об ошибке.
        except BoardException as er:
            print(er)
        # Если всё в порядке, возвращаем True.
        else:
            return True


# Класс доски для получения доски игроками и отрисовки.
class Board:
    def __init__(self):
        g = Game()
        self.size = g.board_size
        self.empty = g.empty_cell
        self.ship = g.ship_cell
        self.board = None

    # Метод вызывающий цикл, который повторяется до тех пор, пока корабли не будут расставлены.
    def cycle_for_getting_board(self):
        while True:
            self.board = [[self.empty for _ in range(self.size)] for _ in range(self.size)]
            board, ships = Ship().random_ship(self.board)
            # Если доска удачно заполнена, возвращаем доску и координаты кораблей.
            if board:
                list_merged = [item for sublist in ships[:3] for item in sublist], ships[3:]
                ships = [item for sublist in list_merged for item in sublist]
                return board, ships

    # Метод для удаления клеток из случайного выбора расстановки кораблей.
    @staticmethod
    def get_free_space(length, moves, rotated):
        g = Game()
        result = []
        # Если корабль занимает одну клетку, получаем клетки вокруг него.
        if length == 1:
            result = (g.contour(rotated))
        # Если клеток больше одной, получаем клетки вокруг каждой из них.
        else:
            for i in rotated:
                result.append(g.contour(i))
        # Вызываем функцию, удаляющую занятые клетки и клетки вокруг из списка доступных клеток.
        moves = g.clean_contour(length, moves, result)
        return moves

    # Метод для замены пустых клеток на клетки корабля.
    def place_ship_on_board(self, board, rotated):
        for i in range(len(rotated)):
            for x, y in rotated:
                board[x][y] = self.ship

    # Метод для рисования доски.
    def draw_board(self, player):
        field_res = " "
        for i in range(self.size):
            field_res += f" |{i + 1:2}"
        field_res += " |"
        for i, row in enumerate(player.board):
            field_res += f"\n{i + 1} | " + " | ".join(row) + " |"
        # Если рисуем доску для Компьютера, то скрываем его корабли.
        if player.name == "Компьютер":
            field_res = field_res.replace(self.ship, self.empty)
        return field_res

    # Метод для вывода поля.
    @staticmethod
    def print_board(one, two):
        print('Поле компьютера:                                                     Поле игрока:')
        print(f'{two[0:27]}  #####################################   {one[0:27]}')
        print(f'{two[28:55]}  # 0 - неизвестная клетка.           #   {one[28:55]}')
        print(f'{two[56:83]}  # • - пустая клетка.                #   {one[56:83]}')
        print(f'{two[84:111]}  # ■ - клетка корабля.               #   {one[84:111]}')
        print(f'{two[112:139]}  # □ - клетка раненного корабля.     #   {one[112:139]}')
        print(f'{two[140:167]}  # X - клетка уничтоженного корабля. #   {one[140:167]}')
        print(f'{two[168:]}  #####################################   {one[168:]}')

    # Метод для изменения клетки поврежденного корабля, на уничтоженные.
    @staticmethod
    def ship_destroyed(x, y, player, enemy):
        g = Game()
        coordinates = []
        cont = g.contour([x, y])
        # Меняем клетки вокруг уничтоженной на пустые.
        for c_x, c_y in cont:
            enemy.board[x][y] = g.destroyed_ship
            # Если клетка рядом пустая, удалим её из доступных для ИИ ходов.
            if (c_x, c_y) in player.moves and not (c_x, c_y) in enemy.ships:
                player.moves.remove((c_x, c_y))
            # Если координаты вне нужного диапазона, пропускаем.
            if c_x < 0 or c_x >= g.board_size or c_y < 0 or c_y >= g.board_size:
                continue
            # Если клетка принадлежит раненному кораблю, меняем её на уничтоженный.
            elif enemy.board[c_x][c_y] == g.damaged_ship:
                enemy.board[c_x][c_y] = g.destroyed_ship
                coord = g.contour((c_x, c_y))
                # И создаем цикл внутри цикла, что бы очистить клетки и вокруг этой.
                for row, col in coord:
                    if (row, col) in player.moves and not (row, col) in enemy.ships:
                        player.moves.remove((row, col))
                    if row < 0 or row >= g.board_size or col < 0 or col >= g.board_size:
                        continue
                    # Если найдена ещё одна клетка поврежденного корабля.
                    elif enemy.board[row][col] == g.damaged_ship:
                        enemy.board[row][col] = g.destroyed_ship
                        coordinates = [row, col]
                    # Если клетка пуста, заменяем на клетку промаха.
                    elif enemy.board[row][col] == g.empty_cell:
                        enemy.board[row][col] = g.miss_cell

            elif enemy.board[c_x][c_y] == g.empty_cell:
                enemy.board[c_x][c_y] = g.miss_cell
        # Если есть координаты ещё одной клетки, помимо двух предыдущих, запускаем похожий цикл для неё.
        if coordinates:
            cont = g.contour(coordinates)
            for c_x, c_y in cont:
                if (c_x, c_y) in player.moves and not (c_x, c_y) in enemy.ships:
                    player.moves.remove((c_x, c_y))
                if c_x < 0 or c_x >= g.board_size or c_y < 0 or c_y >= g.board_size:
                    continue

                elif enemy.board[c_x][c_y] == g.damaged_ship:
                    enemy.board[c_x][c_y] = g.destroyed_ship

                elif enemy.board[c_x][c_y] == g.empty_cell:
                    enemy.board[c_x][c_y] = g.miss_cell


# Класс корабля, для расстановки и передачи координат кораблей.
class Ship:
    def __init__(self):
        self.ships = []

    # Основной метод для получения координат корабля.
    def random_ship(self, board):
        g = Game()
        b = Board()
        moves = g.all_moves()
        for i in g.ship_pool:
            while True:
                # Если клеток для расстановки кораблей не осталось, вернуть False.
                if not moves:
                    return False, False
                # Случайно выбрать из доступных клеток, куда поставить корабль.
                else:
                    cell = choice(moves)
                # Если размер корабля всего 1.
                if i == 1:
                    self.ships.append(cell)
                    board[cell[0]][cell[1]] = g.ship_cell
                    moves = b.get_free_space(i, moves, cell)
                    break
                # Если больше 1, переходим в функцию для выбора направления корабля.
                else:
                    rotated = self.rotate_ship(i, cell, moves)
                    if rotated:
                        moves = b.get_free_space(i, moves, rotated)
                        b.place_ship_on_board(board, rotated)
                        self.ships.append(rotated)
                        break
        return board, self.ships

    # Метод для выбора направления корабля.
    @staticmethod
    def rotate_ship(length, cell, moves):
        cont = Game().contour(cell, True)
        rotated = []
        for i in cont:
            rotated.clear()
            # Если координаты среди доступных.
            if i in moves:
                if length == 2:
                    rotated.append(cell)
                    rotated.append(i)
                    return rotated
                # Если размер больше 2.
                else:
                    a = i[0] - cell[0] + i[0], i[1] - cell[1] + i[1]
                    # Если 3-ю клетку нельзя поставить.
                    if a not in moves:
                        continue
                    else:
                        rotated.append(cell)
                        rotated.append(i)
                        rotated.append(a)
        return list(set(rotated))


# Класс игроков.
class Players:
    def __init__(self, name, board, ships):
        self.name = name
        self.board = board
        self.ships = ships
        self.moves = Game().all_moves()
        if self.name == "Компьютер":
            self.priority = []
            self.previous_move = []
            self.to_kill = False

    # Метод для получения хода.
    @staticmethod
    def get_input(player, enemy):
        # Если игрок человек, то получаем ход, с помощью соответствующего метода.
        if player.name == 'Человек':
            x_y = User.user_move(enemy)
        # Иначе другой метод для ИИ.
        else:
            # Если компьютер в режиме добивания, выбираем ход из приоритетных, иначе просто из доступных.
            if player.to_kill:
                x_y = choice(player.priority)
                player.priority.remove(x_y)
            else:
                x_y = choice(player.moves)
            player.moves.remove(x_y)

        result = Players.check_shoot(x_y, player, enemy)
        return result

    # Метод проверки хода.
    @staticmethod
    def check_shoot(x_y, player, enemy):
        g = Game()
        # Если координаты указывают на клетку корабля.
        if enemy.board[x_y[0]][x_y[1]] == g.ship_cell:
            cont = g.contour(x_y, True)
            # По средствам цикла проверяем если рядом есть другие клетки корабля.
            for x, y in cont:
                elem = ((x_y[0] - x), (x_y[1] - y))
                if x < 0 or x >= g.board_size or y < 0 or y >= g.board_size:
                    continue
                # Если рядом есть клетка целого корабля, возвращаем "попадание".
                elif enemy.board[x][y] == g.ship_cell:
                    enemy.board[x_y[0]][x_y[1]] = g.damaged_ship
                    enemy.ships.remove(x_y)
                    # Если ходит ИИ, вводим его в режим добивания.
                    if player.name == "Компьютер":
                        if player.to_kill:
                            AI.to_kill_enemy(x_y, player)
                        else:
                            player.previous_move = x_y
                            AI.to_kill_enemy(x_y, player)
                    return 'get'
                # Если рядом есть клетка уничтоженного корабля, проверяем нет ли рядом с ним клетки целого корабля.
                elif enemy.board[x][y] == g.destroyed_ship:
                    if enemy.board[x_y[0] - elem[0]][x_y[1] - elem[1]] == g.ship_cell:
                        enemy.ships.remove(x_y)
                        if player.name == "Компьютер":
                            if player.to_kill:
                                AI.to_kill_enemy(x_y, player)
                            else:
                                player.previous_move = x_y
                                AI.to_kill_enemy(x_y, player)
                        return 'get'
            # Если рядом клеток целого корабля не осталось, возвращаем "убил".
            Board.ship_destroyed(x_y[0], x_y[1], player, enemy)
            enemy.board[x_y[0]][x_y[1]] = g.destroyed_ship
            enemy.ships.remove(x_y)
            if player.name == "Компьютер":
                player.to_kill = False
                player.priority.clear()
            return 'kill'
        # Если все условия выше ложны, возвращаем "промах"
        else:
            enemy.board[x_y[0]][x_y[1]] = g.miss_cell
            return 'miss'


# Класс пользователя.
class User(Players):
    # Метод для получения и проверки хода игрока.
    @staticmethod
    def user_move(enemy):
        print('Сделайте ход.')
        print('Подсказка: нужно ввести два числа, где первое - ряд, второе - столбец.')
        print('Или введите "выход" для завершения игры.')
        while True:
            user_input = input('>>> ').replace(" ", "")
            # Отправляем в класс проверки ходов, если метод проверки не вернул True, повторить цикл.
            if user_input == "выход":
                print('Благодарим за игру!')
                exit()
            check_input = CheckMove(user_input, enemy.board)
            valid_input = check_input.check_exception()
            if valid_input:
                x, y = int(user_input[0]) - 1, int(user_input[1]) - 1
                return x, y


# Класс ИИ.
class AI(Players):
    # Метод режима добивания ИИ.
    @staticmethod
    def to_kill_enemy(x_y, player):
        # Если это первое попадание, задаем приоритет для клеток вокруг.
        if not player.to_kill:
            player.to_kill = True
            cont = Game().contour(x_y, True)
            cont = set(cont).intersection(set(player.moves))
            for i in cont:
                player.priority.append(i)
        # Иначе, очищаем приоритет от ходов, где клеток корабля точно быть не может.
        else:
            prev = player.previous_move
            cont = prev[0] - x_y[0], prev[1] - x_y[1]
            n = x_y[0] - cont[0], x_y[1] - cont[1]
            f = prev[0] + cont[0], prev[1] + cont[1]
            player.priority.clear()
            if n in player.moves:
                player.priority.append(n)
            if f in player.moves:
                player.priority.append(f)


# Класс игры.
class Game:
    def __init__(self):
        self.board_size = 6
        self.ship_pool = [3, 2, 2, 1, 1, 1, 1]
        self.empty_cell = '0'
        self.ship_cell = '■'
        self.destroyed_ship = 'X'
        self.damaged_ship = '□'
        self.miss_cell = '•'

    # Метод для получения всевозможных ходов.
    def all_moves(self):
        row, col, moves = [], [], []
        for x in range(self.board_size):
            for y in range(self.board_size):
                row.append(x)
                col.append(y)
                moves = list(product(row, col))
        return list(set(moves))

    # Метод для определения контуров клетки.
    @staticmethod
    def contour(x_y, rotate=False):
        res = []
        row, col = x_y[0], x_y[1]
        # Если метод в режиме ротации выдаем клетки только по горизонтали и вертикали.
        if rotate:
            near = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        # Иначе, выдаем и клетки по углам.
        else:
            near = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
        for x, y in near:
            res += [(x + row, y + col)]
        return res

    # Метод удаляющий из возможных ходов те, совершать которые нет смысла.
    @staticmethod
    def clean_contour(length, moves, cont):
        # Если длинна корабля больше одного, распаковываем списки в списках.
        if length > 1:
            cont = [item for sublist in cont for item in sublist]
        while cont:
            for i in cont:
                if i in moves[:]:
                    moves.remove(i)
                    cont.remove(i)
                else:
                    cont.remove(i)
        return moves

    # Основной метод игры.
    @staticmethod
    def playing_game(user, ai):
        b = Board()
        player, enemy = user, ai
        while True:
            # Если текущий игрок человек, рисуем доску.
            if player.name == "Человек":
                b.print_board(b.draw_board(user), b.draw_board(ai))
            res = Players.get_input(player, enemy)
            # Если результат хода "промах" меняем текущего и следующего игрока местами.
            if res == 'miss':
                print(f'{player.name} - промах!')
                player, enemy = enemy, player
                continue
            elif res == 'get':
                print(f'{player.name} - попал!')
                continue
            elif res == 'kill' or int:
                print(f'{player.name} - убил!')
            # Проверяем если у следующего игрока ещё остались корабли.
            if not enemy.ships:
                b.print_board(b.draw_board(user), b.draw_board(ai))
                return player.name


if __name__ == "__main__":
    while True:
        # Задаем объекты для игроков и запускаем в метод игры.
        us_board = Board().cycle_for_getting_board()
        ai_board = Board().cycle_for_getting_board()
        player1 = Players(name="Человек", board=us_board[0], ships=us_board[1])
        player2 = Players(name="Компьютер", board=ai_board[0], ships=ai_board[1])
        winner = Game().playing_game(player1, player2)
        # Отображаем победителя и спрашиваем если игрок хочет сыграть ещё раз.
        print(f'Игра окончена!\nПобедитель - {winner}!')
        print('Хотите сыграть ещё раз? (Для повтора введите "да")')
        if not input().lower() == 'да':
            print('Благодарим за игру!')
            exit()
