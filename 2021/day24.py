import sys

lines = [line.strip().split() for line in open(sys.argv[1]).readlines()]

memory_index = { 'x': 0, 'y': 1, 'z': 2, 'w': 3 }

cache = {}

def recurse(stack, operation_index, memory, mode = 1):
    if operation_index == len(lines):
        return [] if memory[2] == 0 else None

    line = lines[operation_index]
    key = (operation_index, memory, mode)

    if key not in cache:
        cache[key] = None
        if line[0] == 'inp':
            R = range(9, 0, -1) if mode == 1 else range(1, 10)
            # print(operation_index)

            if mode == -1 and operation_index == 0:
                # R = [3,4]
                R = [int(sys.argv[2])]
            elif mode == -1 and operation_index == 18:
                R = [x for x in range(1, 10) if x >= int(sys.argv[3])]
                # R = [4,5,6,7,8,9]

            for w in R:
                if operation_index < 90: print(' ' * (operation_index // 9), w, stack)
                new_memory = update_at_index(memory, 3, w)
                result = recurse(stack + [w], operation_index + 1, new_memory, mode)
                if result is not None:
                    cache[key] = [w] + result
                    break
        else:
            new_memory = do_op(line, memory)
            cache[key] = recurse(stack, operation_index + 1, new_memory, mode)
    return cache[key]

def update_at_index(slots, index, value):
    result = list(slots)
    result[index] = value
    return tuple(result)

def get_memory(memory, letter):
    return memory[memory_index[letter]]

def op(line, operator, memory):
    a = get_memory(memory, line[1])
    b = int(line[2]) if line[2].isdigit() or line[2][0] == '-' else get_memory(memory, line[2])
    return update_at_index(memory, memory_index[line[1]], operator(a, b))

def mod(a, b):
    if a < 0:
        raise ValueError()
    return a % b

def do_op(line, memory):
    if line[0] == 'add':
        return op(line, lambda a, b: a + b, memory)
    elif line[0] == 'mul':
        return op(line, lambda a, b: a * b, memory)
    elif line[0] == 'div':
        return op(line, lambda a, b: a // b, memory)
    elif line[0] == 'mod':
        return op(line, mod, memory)
    elif line[0] == 'eql':
        return op(line, lambda a, b: 1 if a == b else 0, memory)

result = recurse([], 0, (0,0,0,0), mode=-1)
print(''.join(map(str, result)))
