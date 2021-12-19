from collections import defaultdict

paths = defaultdict(set)
for line in open('day12.input').readlines():
    a, b = line.strip().split('-')
    paths[a].add(b)
    paths[b].add(a)

def count_paths(cave, visited, can_visit_small_cave = False):
    if cave == 'end':
        return 1

    result = 0
    for next_cave in paths[cave]:
        if next_cave not in visited:
            visited.add(next_cave)
            result += count_paths(next_cave, visited, can_visit_small_cave)
            visited.remove(next_cave)
        elif next_cave.isupper():
            result += count_paths(next_cave, visited, can_visit_small_cave)
        elif next_cave.islower() and can_visit_small_cave and next_cave != 'start':
            result += count_paths(next_cave, visited, False)

    return result

print(f"Part 1: {count_paths('start', {'start'})}")
print(f"Part 2: {count_paths('start', {'start'}, can_visit_small_cave=True)}")
