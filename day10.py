from functools import reduce
from collections import deque

matching_close = { '(': ')', '[': ']', '{': '}', '<': '>' }
corruption_cost = { ')': 3, ']': 57, '}': 1197, '>': 25137 }
autocomplete_cost = { ')': 1, ']': 2, '}': 3, '>': 4 }

data = [line.strip() for line in open("day10.input").readlines()]

def score_corrupted(line):
    q = deque()
    for char in line:
        if char in matching_close:
            q.append(char)
        else:
            opening = q.pop()
            if char != matching_close[opening]:
                return corruption_cost[char], []
    return 0, q

def score_autocomplete(line):
    _, q = score_corrupted(line)
    return reduce(lambda score, char: score * 5 + autocomplete_cost[matching_close[char]], reversed(q), 0)

corrupted_scores = map(score_corrupted, data)
print(f"Part 1: {sum(score for score, _ in corrupted_scores)}")

autocomplete_scores = list(sorted(filter(lambda x: x > 0, map(score_autocomplete, data))))
print(f"Part 2: {autocomplete_scores[len(autocomplete_scores) // 2]}")
