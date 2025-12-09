"""
Advent of Code 2025 - Day 1 Part 2

See step2.md for problem description.
"""

import math

def read_input(filename):
    """Read input file and return processed data."""
    with open(filename, 'r') as f:
        lines = f.read().strip().split('\n')
    return lines

def solve(data):
    """
    Solve the puzzle.

    Args:
        data: Processed input data

    Returns:
        Solution answer
    """
    ticker = 50  # current dial position
    count = 0    # total times the dial points at 0

    for line in data:
        direction = line[0]
        steps = int(line[1:])
        start = ticker

        if direction == 'R':
            # distance to next 0 when moving right
            dist = (100 - start) % 100
        else:
            # distance to next 0 when moving left
            dist = start % 100

        # If already at 0, the next time we hit 0 is after 100 steps
        if dist == 0:
            dist = 100

        if steps < dist:
            hits = 0
        else:
            hits = 1 + (steps - dist) // 100

        if direction == 'R':
            ticker = (start + steps) % 100
        else:
            ticker = (start - steps) % 100

        count += hits

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
