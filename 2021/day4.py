from copy import deepcopy
from itertools import product

WIN_ROW = [-1, -1, -1, -1, -1]

with open("day4.input") as file:
    bingo = list(map(int, file.readline().split(',')))

    boards = []

    while file.readline() != '':
        boards.append(list(list(map(int, file.readline().split())) for _ in range(5)))

def rotate(board):
    return list(list(board[row][col] for row in range(5)) for col in range(5))

def min_win_score(bingo, board):
    board = deepcopy(board)

    for index, number in enumerate(bingo):
        for row, col in product(range(5), repeat=2):
            if board[row][col] == number:
                board[row][col] = -1

        if WIN_ROW in board or WIN_ROW in rotate(board):
            score = sum(board[row][col] for row, col in product(range(5), repeat=2) if board[row][col] != -1) * number
            return index, score

print(f"Part 1: {min(min_win_score(bingo, board) for board in boards)}")
print(f"Part 2: {max(min_win_score(bingo, board) for board in boards)}")
