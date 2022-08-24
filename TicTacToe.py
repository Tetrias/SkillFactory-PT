# Игра "крестики-нолики"

import random
import sys


def getGameBoard():
    board = []
    for i in range(3):
        board.append(['[ ]', '[ ]', '[ ]'])
    return board


def drawGameBoard(board):
    print('   1  2  3')
    for y in range(3):
        print(f'{y + 1} ', end='')
        for x in range(3):
            print(board[x][y], end='')
        print()


def isWinner(board, pSign):
    return ((board[0][0] == pSign and board[0][1] == pSign and board[0][2] == pSign) or
            (board[1][0] == pSign and board[1][1] == pSign and board[1][2] == pSign) or
            (board[2][0] == pSign and board[2][1] == pSign and board[2][2] == pSign) or
            (board[0][0] == pSign and board[1][0] == pSign and board[2][0] == pSign) or
            (board[0][1] == pSign and board[1][1] == pSign and board[2][1] == pSign) or
            (board[0][2] == pSign and board[1][2] == pSign and board[2][2] == pSign) or
            (board[0][0] == pSign and board[1][1] == pSign and board[2][2] == pSign) or
            (board[0][2] == pSign and board[1][1] == pSign and board[2][0] == pSign))


def isDraw(board):
    pSign = '[ ]'
    return ((board[0][0] == pSign and board[0][1] == pSign and board[0][2] == pSign) or
            (board[1][0] == pSign and board[1][1] == pSign and board[1][2] == pSign) or
            (board[2][0] == pSign and board[2][1] == pSign and board[2][2] == pSign) or
            (board[0][0] == pSign and board[1][0] == pSign and board[2][0] == pSign) or
            (board[0][1] == pSign and board[1][1] == pSign and board[2][1] == pSign) or
            (board[0][2] == pSign and board[1][2] == pSign and board[2][2] == pSign) or
            (board[0][0] == pSign and board[1][1] == pSign and board[2][2] == pSign) or
            (board[0][2] == pSign and board[1][1] == pSign and board[2][0] == pSign))


def isOnBoard(x, y):
    return 0 <= x <= 2 and 0 <= y <= 2


def isValidMove(board, xmove, ymove):
    if board[xmove][ymove] != '[ ]' or not isOnBoard(xmove, ymove):
        return False


def getPlayerSign():
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


def getMove(board):
    DIGITS1TO3 = '1 2 3'.split()
    while True:
        print('Введите ход (например "11") или "выход", что бы завершить игру.')
        move = input().lower()
        if move == 'выход':
            return move
        if len(move) == 2 and move[0] in DIGITS1TO3 and move[1] in DIGITS1TO3:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, x, y) == False:
                continue
            else:
                break
        else:
            print('Недопустимый ход. Введите номер столбца (1-3) и номер ряда (1-3).')
    return [x, y]


def playGame(player1Sign, player2Sign, turn):
    print(turn + ' играет за "Х" и ходит первым.')
    board = getGameBoard()

    while True:
        stillPlaying = isDraw(board)
        if not stillPlaying:
            return board, 'draw'

        elif turn == 'Игрок 1':
            drawGameBoard(board)
            if isWinner(board, player2Sign):
                return board, 'Игрок 2'
            print('Ход "Игрока 1"')
            move = getMove(board)
            if move == 'выход':
                print('Благодарим за игру!')
                sys.exit()
            else:
                board[move[0]][move[1]] = player1Sign
            turn = 'Игрок 2'

        elif turn == 'Игрок 2':
            drawGameBoard(board)
            if isWinner(board, player1Sign):
                return board, 'Игрок 1'
            print('Ход "Игрока 2"')
            move = getMove(board)
            if move == 'выход':
                print('Благодарим за игру!')
                sys.exit()
            else:
                board[move[0]][move[1]] = player2Sign
            turn = 'Игрок 1'


print('Добро пожаловать в игру "Крестики-нолики"')

while True:
    player1Sign, player2Sign, turn = getPlayerSign()
    while True:

        gameBoard, result = playGame(player1Sign, player2Sign, turn)
        drawGameBoard(gameBoard)

        if result == 'Игрок 1':
            print('"Игрок 1" победил!')
            break

        elif result == 'Игрок 2':
            print('"Игрок 2" победил!')
            break

        else:
            print('Ничья!')
            break

    print('Хотите сыграть еще раз? (да или нет)')
    if not input().lower() == 'да':
        break
