from collections import Counter
from more_itertools import windowed

lines = open('day14.input').readlines()

template = lines[0].strip()
rules = dict([tuple(line.strip().split(' -> ')) for line in lines[2:]])

letter_counts = Counter(template)
pair_counts = Counter(windowed(template, 2))

def apply_rules(pair_counts, letter_counts, rules):
    new_pairs = Counter()
    new_letters = letter_counts.copy()
    for (a, b), count in pair_counts.items():
        if a + b in rules:
            c = rules[a + b]
            new_pairs[a, c] += count
            new_pairs[c, b] += count
            new_letters[c] += count
        else:
            new_pairs[a, b] += count
    return new_pairs, new_letters

def repeat_rules(pair_counts, letter_counts, rules, times):
    for _ in range(times):
        pair_counts, letter_counts = apply_rules(pair_counts, letter_counts, rules)

    most_common_letters = letter_counts.most_common()
    return most_common_letters[0][1] - most_common_letters[-1][1]


print("Part 1:", repeat_rules(pair_counts, letter_counts, rules, 10))
print("Part 2:", repeat_rules(pair_counts, letter_counts, rules, 40))
