# Redo of the task with better tools
from functools import lru_cache
import z3
import sys
from collections import namedtuple

Operation = namedtuple('Operation', ['operation', 'vars'])

MATH_FN = {
    'add': lambda a, b: a + b,
    'mul': lambda a, b: a * b,
    'div': lambda a, b: a / b,
    'mod': lambda a, b: a % b,
    'eql': lambda a, b: z3.If(a == b, constant(1), constant(0)),
}


def parse(line):
    vars = [int(var) if var.isdigit() or var[0] == '-' else var for var in line[1:]]
    return Operation(line[0], vars)

@lru_cache(maxsize=None)
def zint(*name):
    return z3.BitVec(''.join(map(str, name)), 64)

@lru_cache(maxsize=None)
def constant(value):
    return z3.BitVecVal(value, 64)

def get_value(var, index = None):
    if var in indexes:
        if index is None:
            index = indexes[var]
        return zint(var, index)
    else:
        return int(var)

def get_solution(answer_var, solver, solver_fn):
    solver.push()
    solver_fn(answer_var)
    solver.check()
    model = solver.model()
    answer = model[answer_var]
    solver.pop()
    return answer


lines = [parse(line.strip().split()) for line in open(sys.argv[1]).readlines()]

indexes = { 'x': 0, 'y': 0, 'z': 0, 'w': -1 }
solver = z3.Optimize()

for char in 'xyz':
    solver.add(zint(char, 0) == 0)

for op in lines:
    indexes[op.vars[0]] += 1
    if op.operation == 'inp':
        solver.add(get_value('w') >= 1)
        solver.add(get_value('w') <= 9)
    else:
        a, b = op.vars
        a_index = indexes[a]
        fn = MATH_FN[op.operation]

        solver.add(get_value(a, a_index) == fn(get_value(a, a_index - 1), get_value(b)))


solver.add(get_value('z') == 0)

answer = zint('answer')
solver.add(answer == sum(get_value('w', i)*10**(13-i) for i in range(14)))

print('Part 1:', get_solution(answer, solver, solver.maximize))
print('Part 2:', get_solution(answer, solver, solver.minimize))
