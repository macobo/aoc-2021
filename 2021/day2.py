from functools import reduce

MOVEMENT = {
    "forward": (1, 0),
    "down": (0, 1),
    "up": (0, -1)
}

def follow(x, y, command_with_amount):
    command, amount = command_with_amount.split()
    vx, vy = MOVEMENT[command]
    return x + int(amount) * vx, y + int(amount) * vy

commands = open("day2.input").readlines()

x, y = reduce(lambda pos, command: follow(*pos, command), commands, (0, 0))
print(f"Part 1: {x * y}")

def follow_with_aim(x, y, aim, command_with_amount):
    command, amount = command_with_amount.split()
    if command == 'down':
        return x, y, aim + int(amount)
    elif command == 'up':
        return x, y, aim - int(amount)
    else:
        return x + aim * int(amount), y + int(amount), aim


x, y, aim = reduce(lambda pos, command: follow_with_aim(*pos, command), commands, (0, 0, 0))
print(f"Part 2: {x * y}")
