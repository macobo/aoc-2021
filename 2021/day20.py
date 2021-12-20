from collections import defaultdict
from itertools import product
from tqdm import trange


enhancement = []
image_lines = []
image = defaultdict(lambda: '.')

with open('2021/day20.input') as file:
    while (line := file.readline().strip()) != '':
        enhancement.append(line)
    enhancement = ''.join(enhancement)

    while (line := file.readline().strip()) != '':
        image_lines.append(line)

for x in range(len(image_lines)):
    for y in range(len(image_lines[x])):
        image[x,y] = image_lines[x][y]


def translate(pix):
    return '0' if pix == '.' else '1'

def next_pixel(image, x, y):
    binary_number = ''.join(translate(image[x+dx,y+dy]) for dx, dy in product(range(-1, 2), repeat=2))
    return enhancement[int(binary_number, 2)]


def enhance(image, pad):
    min_x = min(x for x, y in image.keys())
    min_y = min(y for x, y in image.keys())
    max_x = max(x for x, y in image.keys())
    max_y = max(y for x, y in image.keys())

    new_image = defaultdict(lambda: pad)

    for x in range(min_x-1, max_x+2):
        for y in range(min_y-1, max_y+2):
            new_image[x,y] = next_pixel(image, x, y)

    return new_image

def enhance_times(image, n):
    for n in trange(n):
        image = enhance(image, enhancement[0] if n % 2 == 0 else '.')
    return list(image.values()).count('#')


print('Part 1:', enhance_times(image, 2))
print('Part 2:', enhance_times(image, 50))
