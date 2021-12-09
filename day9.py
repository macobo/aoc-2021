from itertools import *
from collections import *
from functools import *
from more_itertools import *
from tqdm import trange, tqdm

heightmap = list(map(lambda line: list(map(int, line.strip())), open("day9.input").readlines()))
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
    filled_basins = defaultdict(lambda: -1)
    basin_size = Counter()
    visited = set()
    q = deque([(x, y, i) for i, (_, x, y) in enumerate(lowpoints(heightmap))])

    for x, y, i in q:
        visited.add((x, y))
        basin_size[i] = 1
        filled_basins[x,y] = i
    # print(q)
    while len(q) > 0:
        x, y, i = q.popleft()

        for nx, ny in neighbors(x, y):
            if (nx, ny) not in visited and heightmap[nx][ny] < 9: #and all(heightmap[px][py] > heightmap[nx][ny] for px, py in neighbors(nx, ny) if filled_basins[px, py] != i) and heightmap[nx][ny] < 9:
                q.append((nx, ny, i))
                visited.add((nx, ny))
                basin_size[i] += 1
                filled_basins[nx, ny] = i
    print(sorted(basin_size.values()))
    # print(filled_basins)
    (_, a), (_, b), (_, c) = basin_size.most_common(3)
    print_map(filled_basins)
    return a * b * c

def print_map(filled_basins):
    for x in range(height):
        print(''.join('_' if filled_basins[x,y] == -1 else 'o' for y in range(width)))

print(f"Part 1: {sum(s for s, x, y in lowpoints(heightmap))}")
print(f"Part 2: {find_basins(heightmap)}")
