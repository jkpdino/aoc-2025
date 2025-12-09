"""
Advent of Code 2025 - Day 3 Part 2

See step2.md for problem description.
"""

def read_input(filename):
    """Read input file and return processed data."""
    with open(filename, 'r') as f:
        lines = f.read().strip().split('\n')
    return lines

def maximum_power(number: str) -> int:
    batteries_to_turn_on = 12

    power = 0
    index = 0

    for battery_index in range(batteries_to_turn_on):
        max_digit = 0
        max_digit_index = 0

        for test_index in range(index, len(number) - (batteries_to_turn_on - battery_index) + 1):
            digit = int(number[test_index])
            if digit > max_digit:
                max_digit = digit
                max_digit_index = test_index

        power = 10 * power + max_digit
        index = max_digit_index + 1

    return power


def solve(data):
    """
    Solve the puzzle.

    Args:
        data: Processed input data

    Returns:
        Solution answer
    """
    acc = 0
    for line in data:
        acc += maximum_power(line)
    return acc

if __name__ == "__main__":
    import sys

    if '--test' in sys.argv:
        # Test with example input
        test_data = read_input('test-input.txt')
        test_result = solve(test_data)
        print(f"Test result: {test_result}")
    else:
        # Run with real input
        real_data = read_input('input.txt')
        result = solve(real_data)
        print(f"Result: {result}")
