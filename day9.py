from itertools import product
from collections import deque, Counter

heightmap = [list(map(int, line.strip())) for line in open("day9.input").readlines()]
height, width = len(heightmap), len(heightmap[0])

def neighbors(x, y):
    if x > 0:
        yield x - 1, y
    if x < height - 1:
        yield x + 1, y
    if y > 0:
        yield x, y - 1
    if y < width - 1:
        yield x, y + 1

def lowpoints(heightmap):
    for x, y in product(range(height), range(width)):
        if all(heightmap[nx][ny] > heightmap[x][y] for nx, ny in neighbors(x, y)):
            yield heightmap[x][y] + 1, x, y

def find_basins(heightmap):
    q = deque([(x, y, i) for i, (_, x, y) in enumerate(lowpoints(heightmap))])
    visited = set((x, y) for x, y, _ in q)
    basin_size = Counter([i for _, _, i in q])

    while len(q) > 0:
        x, y, i = q.popleft()

        for nx, ny in neighbors(x, y):
            if (nx, ny) not in visited and heightmap[nx][ny] < 9:
                q.append((nx, ny, i))
                visited.add((nx, ny))
                basin_size[i] += 1

    a, b, c = [value for _, value in basin_size.most_common(3)]
    return a * b * c

print(f"Part 1: {sum(s for s, x, y in lowpoints(heightmap))}")
print(f"Part 2: {find_basins(heightmap)}")
