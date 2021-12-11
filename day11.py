from collections import deque
from itertools import product
from copy import deepcopy

data = [list(map(int, line.strip())) for line in open("day11.input").readlines()]
height, width = 10, 10

def neighbors(x, y):
    for dx, dy in product(range(-1, 2), repeat=2):
        if 0 <= x + dx < height and 0 <= y + dy < width:
            yield x + dx, y + dy

def simulate_step(data):
    flashes = set()
    q = deque()
    for x, y in product(range(height), range(width)):
        data[x][y] += 1
        if data[x][y] > 9:
            flashes.add((x, y))
            q.append((x, y))

    while q:
        x, y = q.popleft()
        data[x][y] = 0
        for nx, ny in neighbors(x, y):
            if (nx, ny) in flashes:
                continue
            data[nx][ny] += 1
            if data[nx][ny] > 9:
                flashes.add((nx, ny))
                q.append((nx, ny))

    return len(flashes)

step1_data = deepcopy(data)
print(f"Part 1: {sum(simulate_step(step1_data) for _ in range(100))}")

step2_data = deepcopy(data)
print("Part 2:", next((i for i in range(1, 1000) if simulate_step(step2_data) == height * width )))
