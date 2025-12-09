"""
Advent of Code 2025 - Day 3 Part 1

See step1.md for problem description.
"""

def read_input(filename):
    """Read input file and return processed data."""
    with open(filename, 'r') as f:
        lines = f.read().strip().split('\n')
    return lines

def maximum_power(number: str) -> int:
    # find the largest digit, earliest, and then find the largest digit after that.

    max_digit = 0
    max_digit_index = 0

    for i in range(len(number) - 1):
        digit = int(number[i])
        if digit > max_digit:
            max_digit = digit
            max_digit_index = i

    # then find the largest digit after that
    max_digit_after = 0
    max_digit_after_index = 0
    
    for i in range(max_digit_index + 1, len(number)):
        digit = int(number[i])
        if digit > max_digit_after:
            max_digit_after = digit
            max_digit_after_index = i

    return max_digit * 10 + max_digit_after


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
