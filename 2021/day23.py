from heapq import heappop, heappush
from itertools import product
from collections import Counter

STACKS = list(enumerate('ABCD'))

initial_stacks = (
    ('D', 'D', 'D', 'B'),
    ('B', 'C', 'B', 'A'),
    ('B', 'B', 'A', 'D'),
    ('C', 'A', 'C', 'C')
)
energy_cost = { 'A': 1, 'B': 10, 'C': 100, 'D': 1000 }

stack_to_slot_costs = {
    'A': [3, 2, 2, 4, 6, 8, 9],
    'B': [5, 4, 2, 2, 4, 6, 7],
    'C': [7, 6, 4, 2, 2, 4, 5],
    'D': [9, 8, 6, 4, 2, 2, 3]
}

closest_stack_slot = {
    'A': [1, 1, 2, 2, 2, 2, 2],
    'B': [2, 2, 2, 3, 3, 3, 3],
    'C': [3, 3, 3, 3, 4, 4, 4],
    'D': [4, 4, 4, 4, 4, 5, 5]
}

def is_blocked_slot_path(slots, start_slot, end_slot):
    slot_range = range(start_slot + 1, end_slot + 1) if start_slot < end_slot else range(end_slot, start_slot)
    return any(slots[i] != '' for i in slot_range)

def is_blocked_slot_to_stack(slots, stack_letter, start_slot):
    end_slot = closest_stack_slot[stack_letter][start_slot]
    return is_blocked_slot_path(slots, start_slot, end_slot)


def is_solved(stacks, N):
    return all(stacks[i] == (letter,) * N for i, letter in STACKS)

def place_slot(slots, pairs):
    result = list(slots)
    for index, value in pairs:
        result[index] = value
    return tuple(result)


def pop_from_stack(stacks, index):
    stacks = list(stacks)
    stacks[index] = stacks[index][1:]
    return tuple(stacks)

def add_to_stack(stacks, index, letter):
    stacks = list(stacks)
    stacks[index] = (letter,) + stacks[index]
    return tuple(stacks)

# Note - only correct if everything in every stack needs to move
def stack_move_cost(stack):
    return sum(energy_cost[letter] for letter in stack)


def next_states(stacks, slots, N):
    # Option 1 - pull out to empty slot!
    for i, stack_letter in STACKS:
        if len(stacks[i]) == 0: continue
        if all(x == stack_letter for x in stacks[i]): continue
        for slot in range(7):
            if slots[slot] != '': continue
            if is_blocked_slot_to_stack(slots, stack_letter, slot): continue

            moved_letter = stacks[i][0]
            cost = stack_to_slot_costs[stack_letter][slot] * energy_cost[moved_letter] + stack_move_cost(stacks[i][1:])
            yield (
                pop_from_stack(stacks, i),
                place_slot(slots, [(slot, moved_letter)]),
                cost
            )

    # Option 2 - slot -> stack
    for slot, (i, stack_letter) in product(range(7), STACKS):
        if slots[slot] == '': continue
        if len(stacks[i]) == N: continue
        if is_blocked_slot_to_stack(slots, stack_letter, slot): continue
        if slots[slot] != stack_letter: continue
        if any(x != stack_letter for x in stacks[i]): continue

        moved_letter = slots[slot]
        cost = stack_to_slot_costs[stack_letter][slot] * energy_cost[moved_letter] + stack_move_cost(stacks[i])
        yield (
            add_to_stack(stacks, i, moved_letter),
            place_slot(slots, [(slot, '')]),
            cost
        )


def solve(init_stacks, init_slots = ('',) * 7, N = len(initial_stacks[0])):
    q = [(0, init_stacks, init_slots)]
    seen = set()

    while q:
        cost_so_far, stacks, slots = heappop(q)

        if is_solved(stacks, N):
            return cost_so_far

        if (stacks, slots) in seen:
            continue

        seen.add((stacks, slots))

        for new_stacks, new_slots, cost in next_states(stacks, slots, N):
            if (new_stacks, new_slots) in seen:
                continue
            heappush(q, (cost_so_far + cost, new_stacks, new_slots))


initial_stacks = (
    ('D', 'D', 'D', 'B'),
    ('A', 'C', 'B', 'A'),
    ('B', 'B', 'A', 'D'),
    ('C', 'A', 'C', 'C')
)

print(solve(initial_stacks))
