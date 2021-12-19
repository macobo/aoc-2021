from heapq import heappop, heappush

lines = open("day15.input").readlines()
graph = [list(map(int, line.strip())) for line in lines]

def wrap(n):
    while n > 9:
        n -= 9
    return n

def neighbors(x, y, width, height):
    if x > 0:
        yield x - 1, y
    if x < height - 1:
        yield x + 1, y
    if y > 0:
        yield x, y - 1
    if y < width - 1:
        yield x, y + 1


def graph_search(graph):
    height, width = len(graph), len(graph[0])
    visited = set()
    q = [(0, (0, 0))]

    while q:
        cost, (x, y) = heappop(q)

        if (x, y) in visited: continue

        if x == height - 1 and y == width - 1:
            return cost

        visited.add((x, y))

        for nx, ny in neighbors(x, y, width, height):
            if (nx, ny) not in visited:
                heappush(q, (cost + graph[nx][ny], (nx, ny)))

print(f"Part 1: {graph_search(graph)}")

height, width = len(graph), len(graph[0])
new_graph = []
for x in range(height * 5):
    new_row = [wrap(graph[x % height][y % width] + x // height + y // width) for y in range(width * 5)]
    new_graph.append(new_row)

print(f"Part 2: {graph_search(new_graph)}")
