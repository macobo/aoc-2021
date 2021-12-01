data = list(map(int, open("day1.input").readlines()))

def number_times_increased(data):
    return len(list(filter(lambda pair: pair[1] > pair[0], zip(data, data[1:]))))

def sliding_window(data, window_size):
    return [sum(data[i:i+window_size]) for i in range(len(data) - window_size + 1)]

print(f"Answer for day 1 A: {number_times_increased(data)}")
print(f"Answer for day 1 B: {number_times_increased(sliding_window(data, 3))}")
