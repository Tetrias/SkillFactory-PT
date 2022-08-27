# Игра "крестики-нолики"

import random
import sys


def get_game_field():
    # Получить игровое поле:
    field = []
    for i in range(3):
        field.append(['[ ]', '[ ]', '[ ]'])
    return field


def draw_game_field(field):
    # Нарисовать игровое поле:
    print('   1  2  3')
    for y in range(3):
        print(f'{y + 1} ', end='')
        for x in range(3):
            print(field[x][y], end='')
        print()


def is_winner(field, p_sign):
    # Проверить победителя:
    return ((field[0][0] == p_sign and field[0][1] == p_sign and field[0][2] == p_sign) or
            (field[1][0] == p_sign and field[1][1] == p_sign and field[1][2] == p_sign) or
            (field[2][0] == p_sign and field[2][1] == p_sign and field[2][2] == p_sign) or
            (field[0][0] == p_sign and field[1][0] == p_sign and field[2][0] == p_sign) or
            (field[0][1] == p_sign and field[1][1] == p_sign and field[2][1] == p_sign) or
            (field[0][2] == p_sign and field[1][2] == p_sign and field[2][2] == p_sign) or
            (field[0][0] == p_sign and field[1][1] == p_sign and field[2][2] == p_sign) or
            (field[0][2] == p_sign and field[1][1] == p_sign and field[2][0] == p_sign))


def is_field_full(field):
    # Проверить заполнено ли поле:
    blank = '[ ]'
    if blank in str(field):
        return True
    else:
        return False


def is_valid_move(field, x_move, y_move):
    # Проверить возможность хода:
    if field[x_move][y_move] != '[ ]' or not (0 <= x_move <= 2 and 0 <= y_move <= 2):
        return False


def get_player_sign():
    # Выбор знака игроком и случайное определение первого хода:
    sign = ''
    while sign == '':
        print('Игрок 1 выбирает знак. "Х" или "О".')
        letter = input().lower()
        if "х" in letter or "x" in letter:
            sign = '[X]'
        elif "o" in letter or "о" in letter:
            sign = '[O]'
        else:
            print('Не верный выбор знака, вам нужно выбрать "О" или "Х".')
    first_move = random.randint(0, 1)

    if sign == '[X]':
        return ['[X]', '[O]', 'Игрок 1' if first_move == 0 else 'Игрок 2']
    else:
        return ['[O]', '[X]', 'Игрок 1' if first_move == 0 else 'Игрок 2']


def get_move(field):
    # Получение и проверка хода игрока:
    DIGITS1TO3 = '1 2 3'.split()
    while True:
        print('Введите ход (например "11", где первое число ряд, второе столбец.) или "выход", что бы завершить игру.')
        move = input().lower()
        if move == 'выход':
            return move
        if len(move) == 2 and move[0] in DIGITS1TO3 and move[1] in DIGITS1TO3:
            x = int(move[1]) - 1
            y = int(move[0]) - 1
            if is_valid_move(field, x, y) is False:
                continue
            else:
                break
        else:
            print('Недопустимый ход. Введите номер ряда (1-3) и номер столбца (1-3).')
    return [x, y]


def make_move(field, player_sign):
    # Выполнение хода игрока:
    move = get_move(field)
    if move == 'выход':
        print('Благодарим за игру!')
        sys.exit()
    else:
        field[move[0]][move[1]] = player_sign


def play_game(player_1_sign, player_2_sign, player_turn):
    # Основная функция для игры:
    print(f'"Игрок 1" играет за {player_1_sign}, "Игрок 2" за {player_2_sign}.\n {player_turn} ходит первым.')
    field = get_game_field()
    while True:
        draw_game_field(field)
        # Проверка победителя или заполненности поля:
        if is_winner(field, player_1_sign):
            return field, 'Игрок 1'
        elif is_winner(field, player_2_sign):
            return field, 'Игрок 2'
        elif not is_field_full(field):
            return field, 'draw'
        # Получение хода, совершение хода и передача хода следующему игроку:
        else:
            if player_turn == 'Игрок 1':
                print('Ход "Игрока 1"')
                make_move(field, player_1_sign)
                player_turn = 'Игрок 2'
            else:
                print('Ход "Игрока 2"')
                make_move(field, player_2_sign)
                player_turn = 'Игрок 1'


print('Добро пожаловать в игру "Крестики-нолики"')

while True:
    # Основной код в виде цикла, для возможности повтора игры по завершению.
    p1, p2, turn = get_player_sign()
    while True:
        gameField, result = play_game(p1, p2, turn)
        draw_game_field(gameField)

        # Вывод основных результатов.
        if result == 'Игрок 1':
            print('"Игрок 1" победил!')
            break

        elif result == 'Игрок 2':
            print('"Игрок 2" победил!')
            break

        else:
            print('Ничья!')
            break
    # Предложение повторить игру.
    print('Хотите сыграть еще раз? (да или нет)')
    if not input().lower() == 'да':
        break
