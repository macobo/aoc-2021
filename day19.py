from collections import defaultdict
from itertools import combinations, product, permutations
from tqdm import trange

def read_input():
    relative_beacon_positions = defaultdict(list)
    beacon = 0

    for line in open("day19.input").readlines():
        if line.startswith('---'): continue
        if line == '\n':
            beacon += 1
            continue
        relative_position = tuple(map(int, line.split(',')))
        relative_beacon_positions[beacon].append(relative_position)
    return relative_beacon_positions

def reorient(line_of_sight, xyz, mul):
    x, y, z = xyz
    mx, my, mz = mul
    return [(pos[x] * mx, pos[y] * my, pos[z] * mz) for pos in line_of_sight]

def reorientations(line_of_sight):
    for xyz in permutations([0, 1, 2]):
        for mul in product([1, -1], repeat=3):
            yield reorient(line_of_sight, xyz, mul)

def get_todo_indexes(scanner_positions, relative_beacon_positions):
    return [i for i in range(len(relative_beacon_positions)) if i not in scanner_positions]

def estimate_scanner_position(known_beacon, relative_beacon):
    kx, ky, kz = known_beacon
    rx, ry, rz = relative_beacon
    return kx - rx, ky - ry, kz - rz

def get_absolute_beacon_position(scanner_pos, relative_beacon):
    ax, ay, az = scanner_pos
    rx, ry, rz = relative_beacon
    return ax + rx, ay + ry, az + rz

def translate_beacon_positions(scanner_pos, line_of_sight):
    return [get_absolute_beacon_position(scanner_pos, rel) for rel in line_of_sight]


def do_next_update():
    for todo_index in get_todo_indexes(scanner_positions, relative_beacon_positions):
        for line_of_sight in reorientations(relative_beacon_positions[todo_index]):
            for k, known_beacon in enumerate(known_beacon_positions):
                if k < 11: continue # Optimization: Don't need to check all options
                for r in range(len(line_of_sight) - 11):
                    scanner_pos = estimate_scanner_position(known_beacon, line_of_sight[r])
                    translated_positions = set(translate_beacon_positions(scanner_pos, line_of_sight))

                    if len(known_beacon_positions & translated_positions) >= 12:
                        known_beacon_positions.update(translated_positions)
                        scanner_positions[todo_index] = scanner_pos
                        return

def manhattan_distance(pos_a, pos_b):
    return sum(abs(a - b) for a, b in zip(pos_a, pos_b))

relative_beacon_positions = read_input()
scanner_positions = { 0: (0,0,0) }
known_beacon_positions = set(relative_beacon_positions[0])

for _ in trange(1, len(relative_beacon_positions)):
    do_next_update()

print("Part 1:", len(known_beacon_positions))
print("Part 2:", max(manhattan_distance(a, b) for a, b in combinations(scanner_positions.values(), 2)))
