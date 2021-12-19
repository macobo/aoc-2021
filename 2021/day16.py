from functools import reduce
from more_itertools import take

hex_packet = open('day16.input').readline().strip()

OPERATIONS = {
    0: lambda values: sum(values),
    1: lambda values: reduce(lambda a, b: a * b, values),
    2: lambda values: min(values),
    3: lambda values: max(values),
    5: lambda values: 1 if values[0] > values[1] else 0,
    6: lambda values: 1 if values[0] < values[1] else 0,
    7: lambda values: 1 if values[0] == values[1] else 0,
}

LAST_LITERAL_BYTE_START = '0'
OPERATOR_TYPE_BY_LENGTH = '0'


def calculate_operation(operation_type, values):
    return OPERATIONS[operation_type](values)

def pad(value, length, fill):
    return fill * (length - len(value)) + value

def to_binstring(hexstring):
    return ''.join(pad(bin(int(char, 16))[2:], 4, '0') for char in hexstring)

def take_bits(binary_iter, length):
    return ''.join(take(length, binary_iter))

def take_int(binary_iter, length):
    binstring = take_bits(binary_iter, length)
    if binstring == '':
        return None
    else:
        return int(binstring, 2)

def process_packet(binary_iter, depth = 0):
    version = take_int(binary_iter, 3)
    typeid = take_int(binary_iter, 3)

    if typeid == None:
        return None, None

    if typeid == 4:
        result = []
        while True:
            bits = take_bits(binary_iter, 5)
            result.append(bits[1:])
            if bits[0] == LAST_LITERAL_BYTE_START:
                break

        return version, int(''.join(result), 2)
    else:
        subpacket_versions = []
        subpacket_results = []
        if take_bits(binary_iter, 1) == OPERATOR_TYPE_BY_LENGTH:
            subpacket_bits = take_int(binary_iter, 15)
            subpacket_hexstring = iter(take_bits(binary_iter, subpacket_bits))
            while True:
                sub_version_sum, value = process_packet(subpacket_hexstring, depth + 1)
                if sub_version_sum is None:
                    break
                subpacket_versions.append(sub_version_sum)
                subpacket_results.append(value)
        else:
            subpackets = take_int(binary_iter, 11)
            for _ in range(subpackets):
                sub_version_sum, value = process_packet(binary_iter, depth + 1)
                subpacket_versions.append(sub_version_sum)
                subpacket_results.append(value)

        return (sum(subpacket_versions) + version, calculate_operation(typeid, subpacket_results))

part1, part2 = process_packet(iter(to_binstring(hex_packet)))
print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
