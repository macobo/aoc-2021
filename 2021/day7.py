from itertools import *
from collections import *
from functools import *
from more_itertools import *

data = list(map(int, open("day7.input").readline().split(',')))

min_value, max_value = min(data), max(data)
min_cost = min(sum(abs(pos - target) for pos in data) for target in range(min_value, max_value+1))

print(f"Part 1: {min_cost}")

def cost_fn(pos, target):
    diff = abs(pos - target)
    return diff * (diff + 1) // 2

min_cost2 = min(sum(cost_fn(pos, target) for pos in data) for target in range(min_value, max_value+1))
print(f"Part 2: {min_cost2}")
