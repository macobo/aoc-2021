from collections import Counter

FLIPPED = { '0': '1', '1': '0' }

data = [row.strip() for row in open("day3.input").readlines()]

columns = len(data[0])
counters = [Counter(data[row][col] for row in range(len(data))) for col in range(columns)]

def get_number(counters, flip = False):
    value = [counter.most_common()[0][0] for counter in counters]
    if flip:
        value = [FLIPPED[x] for x in value]
    return int(''.join(value), 2)

gamma = get_number(counters, False)
epsilon = get_number(counters, True)

print(f"Part 1: {gamma * epsilon}")

def search(data, find_most_common):
    for column in range(len(data[0])):
        matching_bit = find_most_common_value(data, column, flip=not find_most_common)
        data = [row for row in data if row[column] == matching_bit]

        print([column, matching_bit, data])

        if len(data) == 1:
            return int(data[0], 2)

def find_most_common_value(data, column, flip = False):
    counter = Counter(data[row][column] for row in range(len(data)))
    if counter['0'] > counter['1']:
        value = '0'
    else:
        value = '1'
    if flip:
        value = FLIPPED[value]
    return value

oxygen_rating = search(data, find_most_common=True)
co2_rating = search(data, find_most_common=False)

print(f"Part 2: {oxygen_rating * co2_rating}")
