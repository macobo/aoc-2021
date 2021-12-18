from ast import literal_eval
from copy import deepcopy
from itertools import product

def get_paths(data):
    if isinstance(data, int):
        yield 0, tuple()
    else:
        index = 0
        for i, item in enumerate(data):
            for _, path in get_paths(item):
                yield index, (i,) + path
                index += 1

def eval_path(data, path, value_setter = None):
    subresult = data[path[0]]

    if len(path) == 1:
        if value_setter is not None:
            data[path[0]] = value_setter(subresult)
        return subresult
    else:
        return eval_path(subresult, path[1:], value_setter)

def get_first_operation(data, paths):
    for i, path in sorted(paths.items()):
        if len(path) > 4:
            return 'explode', i, path[:4]

    for i, path in sorted(paths.items()):
        if eval_path(data, path) >= 10:
            return 'split', i, path

    return None, None, None

def apply_first_operation(data):
    paths = dict(get_paths(data))
    operation, index, path = get_first_operation(data, paths)
    data = deepcopy(data)

    if operation == 'explode':
        a, b = eval_path(data, path, lambda _: 0)

        if index > 0:
            eval_path(data, paths[index-1], lambda left: left + a)
        if index+2 < len(paths):
            eval_path(data, paths[index+2], lambda right: right + b)
    elif operation == 'split':
        eval_path(data, path, lambda value: [value // 2, value // 2 + value % 2])

    return operation is not None, data

def apply_reductions(data):
    has_applied_rule = True
    while has_applied_rule:
        has_applied_rule, data = apply_first_operation(data)
    return data

def add(snailfishes):
    result = apply_reductions(snailfishes[0])
    for i in range(1, len(snailfishes)):
        result = apply_reductions([result, apply_reductions(snailfishes[i])])
    return result

def magnitude(data):
    if isinstance(data, int):
        return data
    else:
        return 3 * magnitude(data[0]) + 2 * magnitude(data[1])


snailfishes = list(map(literal_eval, open('day18.input').readlines()))

print(f"Part 1: {magnitude(add(snailfishes))}")

largest_sum = max(magnitude(add([a, b])) for a, b in product(snailfishes, repeat=2) if a != b)
print(f"Part 2: {largest_sum}")
