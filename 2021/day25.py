import sys
from itertools import product

lines = open(sys.argv[1]).readlines()
data = [line.strip() for line in lines]

height, width = len(data), len(data[0])

positions = {
    (x, y): data[x][y]
    for x, y in product(range(height), range(width))
    if data[x][y] in ('>', 'v')
}

def neighbors(positions, x, y):
    nx, ny = x, y
    if positions[x,y] == '>':
        ny = (y + 1) % width
    else:
        nx = (x + 1) % height
    if (nx, ny) not in positions:
        return True, nx, ny
    else:
        return False, x, y

def simulate(positions, direction):
    move_count = 0
    new_positions = {}
    for (x, y), dir in positions.items():
        if dir == direction:
            moved, nx, ny = neighbors(positions, x, y)
            new_positions[nx, ny] = dir

            if moved:
                move_count += 1
        else:
            new_positions[x, y] = dir

    return new_positions, move_count


print(sys.argv[1])
step = 0
moved = True
while moved:
    positions, move_count = simulate(positions, '>')
    positions, move_count2 = simulate(positions, 'v')
    moved = (move_count + move_count2) > 0
    step += 1

print(step)
