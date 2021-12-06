from collections import Counter

data = Counter(map(int, open("day6.input").readline().split(',')))

def simulate_day(data):
    new_data = Counter()
    for day, value in sorted(data.items()):
        if day == 0:
            new_data[8] += value
            new_data[6] += value
        else:
            new_data[day - 1] += value
    return new_data

def simulate_days(data, days):
    for _ in range(days):
        data = simulate_day(data)
    return sum(data.values())

print(f"Part 1: {simulate_days(data, 80)}")
print(f"Part 2: {simulate_days(data, 256)}")
