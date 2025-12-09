"""
Advent of Code 2025 - Day 2 Part 1

See step1.md for problem description.
"""

def read_input(filename):
    """Read input file and return processed data."""
    with open(filename, 'r') as f:
        lines = f.read().strip().split(',')
    return lines

def repeated_number(number: str) -> int:
    # if the first half of the number is the same as the second half, return the number, otherwise return 0
    if len(number) % 2 != 0:
        return 0
    half = len(number) // 2
    if number[:half] == number[half:]:
        return int(number)
    return 0

def solve(data):
    """
    Solve the puzzle.

    Args:
        data: Processed input data

    Returns:
        Solution answer
    """

    acc = 0

    for pair in data:
        pair0, pair1 = pair.split('-')

        pair0 = int(pair0)
        pair1 = int(pair1)

        for i in range(pair0, pair1 + 1):
            acc += repeated_number(str(i))

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
