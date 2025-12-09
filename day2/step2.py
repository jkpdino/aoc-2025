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
    # Alright, now lets think about this. We need to check if the number is made of some sequence of digits repeated at least twice.

    for i in range(1, len(number) // 2 + 1):
        slice = number[0:i]

        if len(number) % len(slice) != 0:
            continue

        repeated_times = len(number) // len(slice)

        if slice * repeated_times == number:
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
