# Игра "крестики-нолики"

import random
import sys


def getGameField():
    # Получить игровое поле:
    field = []
    for i in range(3):
        field.append(['[ ]', '[ ]', '[ ]'])
    return field


def drawGameField(field):
    # Нарисовать игровое поле:
    print('   1  2  3')
    for y in range(3):
        print(f'{y + 1} ', end='')
        for x in range(3):
            print(field[x][y], end='')
        print()


def isWinner(field, pSign):
    # Проверить победителя:
    return ((field[0][0] == pSign and field[0][1] == pSign and field[0][2] == pSign) or
            (field[1][0] == pSign and field[1][1] == pSign and field[1][2] == pSign) or
            (field[2][0] == pSign and field[2][1] == pSign and field[2][2] == pSign) or
            (field[0][0] == pSign and field[1][0] == pSign and field[2][0] == pSign) or
            (field[0][1] == pSign and field[1][1] == pSign and field[2][1] == pSign) or
            (field[0][2] == pSign and field[1][2] == pSign and field[2][2] == pSign) or
            (field[0][0] == pSign and field[1][1] == pSign and field[2][2] == pSign) or
            (field[0][2] == pSign and field[1][1] == pSign and field[2][0] == pSign))


def isDraw(field):
    # Проверить возможность продолжать игру:
    pSign = '[ ]'
    return ((field[0][0] == pSign and field[0][1] == pSign and field[0][2] == pSign) or
            (field[1][0] == pSign and field[1][1] == pSign and field[1][2] == pSign) or
            (field[2][0] == pSign and field[2][1] == pSign and field[2][2] == pSign) or
            (field[0][0] == pSign and field[1][0] == pSign and field[2][0] == pSign) or
            (field[0][1] == pSign and field[1][1] == pSign and field[2][1] == pSign) or
            (field[0][2] == pSign and field[1][2] == pSign and field[2][2] == pSign) or
            (field[0][0] == pSign and field[1][1] == pSign and field[2][2] == pSign) or
            (field[0][2] == pSign and field[1][1] == pSign and field[2][0] == pSign))


def isValidMove(field, xmove, ymove):
    # Проверить возможность хода:
    if field[xmove][ymove] != '[ ]' or not (0 <= xmove <= 2 and 0 <= ymove <= 2):
        return False


def getPlayerSign():
    # Распределение знаков между игроками и первого хода:
    sign = ''
    while not (sign == '[X]' or sign == '[O]'):
        randomizer = random.randint(0, 1)
        if randomizer == 0:
            sign = '[X]'
        else:
            sign = '[O]'
    if sign == '[X]':
        return ['[X]', '[O]', 'Игрок 1']
    else:
        return ['[O]', '[X]', 'Игрок 2']


def getMove(field):
    # Получение и проверка хода игрока:
    DIGITS1TO3 = '1 2 3'.split()
    while True:
        print('Введите ход (например "11") или "выход", что бы завершить игру.')
        move = input().lower()
        if move == 'выход':
            return move
        if len(move) == 2 and move[0] in DIGITS1TO3 and move[1] in DIGITS1TO3:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if not isValidMove(field, x, y):
                continue
            else:
                break
        else:
            print('Недопустимый ход. Введите номер столбца (1-3) и номер ряда (1-3).')
    return [x, y]


def playGame(player1Sign, player2Sign, turn):
    # Основная функция для игры:
    print(turn + ' играет за "Х" и ходит первым.')
    field = getGameField()

    while True:
        # Проверка возможности продолжать игру:
        stillPlaying = isDraw(field)
        if not stillPlaying:
            return field, 'draw'

        # Ход первого игрока:
        elif turn == 'Игрок 1':
            drawGameField(field)
            # Проверить не победил ли второй игрок на прошлом ходу, перед ходом первого игрока:
            if isWinner(field, player2Sign):
                return field, 'Игрок 2'
            print('Ход "Игрока 1"')
            move = getMove(field)
            # Проверить если игрок хочет выйти, если нет, завершить ход:
            if move == 'выход':
                print('Благодарим за игру!')
                sys.exit()
            else:
                field[move[0]][move[1]] = player1Sign
            turn = 'Игрок 2'

        # Ход второго игрока
        elif turn == 'Игрок 2':
            drawGameField(field)
            # Проверить не победил ли первый игрок на прошлом ходу, перед ходом второго игрока:
            if isWinner(field, player1Sign):
                return field, 'Игрок 1'
            print('Ход "Игрока 2"')
            move = getMove(field)
            # Проверить если игрок хочет выйти, если нет, завершить ход:
            if move == 'выход':
                print('Благодарим за игру!')
                sys.exit()
            else:
                field[move[0]][move[1]] = player2Sign
            turn = 'Игрок 1'


print('Добро пожаловать в игру "Крестики-нолики"')

while True:
    # Основной код в виде цикла, для возможности повтора игры по завершению.
    player1Sign, player2Sign, turn = getPlayerSign()
    while True:
        gameField, result = playGame(player1Sign, player2Sign, turn)
        drawGameField(gameField)

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
