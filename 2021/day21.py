import sys
from itertools import product
from copy import copy


def dice():
    while True:
        for roll in range(1, 101):
            yield roll


def step(pos, score, rolls):
    roll_sum = sum([next(roller), next(roller), next(roller)])
    new_position = (pos - 1 + roll_sum) % 10 + 1
    return new_position, score + new_position, rolls + 3

def add(tuples):
    return tuple(sum(col) for col in zip(*tuples))

dp_cache = {}
def dp(positions, scores, player):
    if scores[0] >= 21:
        return (1, 0)
    if scores[1] >= 21:
        return (0, 1)

    key = (positions[0], positions[1], scores[0], scores[1], player)
    if key not in dp_cache:
        results = []
        for quantum_roll in product(range(1,4), repeat=3):
            new_pos = copy(positions)
            new_scores = copy(scores)
            new_pos[player] = (new_pos[player] - 1 + sum(quantum_roll)) % 10 + 1
            new_scores[player] += new_pos[player]
            results.append(dp(new_pos, new_scores, (player + 1)%2))
        dp_cache[key] = add(results)
    return dp_cache[key]

start_position = [int(line.strip().split(': ')[1]) for line in open(sys.argv[1]).readlines()]

roller = dice()
rolls = player = 0
scores = [0, 0]
position = copy(start_position)
while max(scores) < 1000:
    position[player], scores[player], rolls = step(position[player], scores[player], rolls)
    player = (player + 1) % 2
print('Part 1:', min(scores) * rolls)

wins_part_2 = dp(start_position, [0,0], 0)
print('Part 2:', max(wins_part_2))
