plane = set()
folds = []

lines = iter(open('day13.input').readlines())
for line in lines:
    if line == '\n': break
    x, y = list(map(int, line.strip().split(',')))
    plane.add((y, x))

for line in lines:
    a, b = line.strip().split('=')
    folds.append((a[-1], int(b)))

fold_along = lambda fc, p: 2 * fc - p

def fold(x, y, new_plane, fold_kind, fold_coordinate):
    if fold_kind == 'y':
        if x < fold_coordinate:
            new_plane.add((x, y))
        else:
            new_plane.add((fold_along(fold_coordinate, x), y))
    else:
        if y < fold_coordinate:
            new_plane.add((x, y))
        else:
            new_plane.add((x, fold_along(fold_coordinate, y)))

def do_folds(plane, folds):
    for fold_kind, fold_coordinate in folds:
        new_plane = set()
        for x, y in plane:
            fold(x, y, new_plane, fold_kind, fold_coordinate)
        plane = new_plane
    return plane

print(f"Part 1: {len(do_folds(plane, folds[:1]))}")
print(f"Part 2:")
plane2 = do_folds(plane, folds)
for x in range(6):
    for y in range(40):
        if (x, y) in plane2:
            print('=', end='')
        else:
            print(' ', end='')
    print('')
