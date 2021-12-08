from itertools import *
from collections import *
from functools import *
from more_itertools import *

CHARS = "abcdefg"

mappings = {
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9,
}

data = []
for line in open('day8.input'):
    parts = line.strip().split()
    inputs, outputs = parts[:10], parts[11:]
    data.append((inputs, outputs))

def count_1478(line):
    inputs, outputs = line
    return sum(1 for part in outputs if len(part) in [2,4,3,7])

def map_to_permutation(input, lookup):
    return ''.join(sorted(lookup[char] for char in input))

def decode(line):
    inputs, outputs = line
    for permutation in distinct_permutations(CHARS):
        lookup = {char: CHARS[i] for i, char in enumerate(permutation)}
        mapped_input = [map_to_permutation(input, lookup) for input in inputs]
        mapped_output = [map_to_permutation(output, lookup) for output in outputs]

        if all(x in mappings for x in mapped_output) and all(x in mappings for x in mapped_input):
            return int(''.join(str(mappings[x]) for x in mapped_output))


print(f"Part 1: {sum(map(count_1478, data))}")
print(f"Part 2: {sum(map(decode, data))}")
