from tqdm import trange

def parse_range(part):
    _, range = part.split('=')
    start, end = range.split('..')
    return int(start), int(end)

def simulate_trajectory(dx, dy):
    x, y = 0, 0
    max_height = 0

    while x <= max_x and y >= min_y:
        if min_x <= x <= max_x and min_y <= y <= max_y:
            return max_height

        x, y = x + dx, y + dy
        dx, dy = max([0, dx - 1]), dy - 1
        max_height = max([max_height, y])

def compact(iterator):
    return filter(lambda value: value is not None, iterator)

_, statement = open("day17.input").readline().strip().split(': ')
(min_x, max_x), (min_y, max_y) = list(map(parse_range, statement.split(', ')))

heights_reached = list(compact(simulate_trajectory(dx, dy) for dx in trange(max_x + 1) for dy in range(min_y, 200)))
print(f"Part 1: {max(heights_reached)}")
print(f"Part 2: {len(heights_reached)}")
