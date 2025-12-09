"""
Advent of Code 2025 - Day 1 Part 1

See step1.md for problem description.
"""

def read_input(filename):
    """Read input file and return processed data."""
    with open(filename, 'r') as f:
        lines = f.read().strip().split('\n')
    return lines


def move(ticker, direction, steps):
    if direction == 'L':
        ticker -= steps
    else:
        ticker += steps
    return ticker % 100

def solve(data):
    """
    Solve the puzzle.

    Args:
        data: Processed input data

    Returns:
        Solution answer
    """
    ticker = 50
    count = 0

    for line in data:
        direction = line[0]
        steps = int(line[1:])

        ticker = move(ticker, direction, steps)

        if ticker == 0:
            count += 1

    return count



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
