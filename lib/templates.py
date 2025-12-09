"""
Template generator for Advent of Code solution files.
"""

STEP_TEMPLATE = '''"""
Advent of Code 2025 - Day {day} Part {part}

See step{part}.md for problem description.
"""

def read_input(filename):
    """Read input file and return processed data."""
    with open(filename, 'r') as f:
        lines = f.read().strip().split('\\n')
    return lines

def solve(data):
    """
    Solve the puzzle.

    Args:
        data: Processed input data

    Returns:
        Solution answer
    """
    # TODO: Implement solution
    pass

if __name__ == "__main__":
    import sys

    if '--test' in sys.argv:
        # Test with example input
        test_data = read_input('test-input.txt')
        test_result = solve(test_data)
        print(f"Test result: {{test_result}}")
    else:
        # Run with real input
        real_data = read_input('input.txt')
        result = solve(real_data)
        print(f"Result: {{result}}")
'''


def generate_step_template(day, part):
    """
    Generate template for step1.py or step2.py.

    Args:
        day: Day number (1-12)
        part: Part number (1 or 2)

    Returns:
        str: Template content
    """
    return STEP_TEMPLATE.format(day=day, part=part)
