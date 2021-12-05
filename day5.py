from collections import *

def parse(line):
    a, b = line.split(' -> ')
    return tuple(map(int, a.split(','))), tuple(map(int, b.split(',')))

data = list(map(parse, open("day5.input").readlines()))

def fill(line, board, fill_diagonals):
    (sx, sy), (ex, ey) = line
    if sx == ex:
        start, end = list(sorted([sy, ey]))
        for y in range(start, end+1):
            board[sx, y] += 1
    elif sy == ey:
        start, end = list(sorted([sx, ex]))
        for x in range(start, end+1):
            board[x, sy] += 1
    # part 2
    elif fill_diagonals and abs(sx - ex) == abs(sy - ey):
        dx = 1 if ex > sx else -1
        dy = 1 if ey > sy else -1
        while sx != ex and sy != ey:
            board[sx,sy] +=1
            sx, sy = sx + dx, sy + dy
        board[sx,sy] +=1

def filled_board(lines, fill_diagonals = False):
    filled_board = defaultdict(lambda: 0)
    for line in lines:
        fill(line, filled_board, fill_diagonals)
    return filled_board

def count(board):
    return sum(1 for v in board.values() if v > 1)

print(f"Part 1: {count(filled_board(data))}")
print(f"Part 2: {count(filled_board(data, fill_diagonals=True))}")
