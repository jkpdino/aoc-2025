# Advent of Code 2025 Test Harness

A Python CLI tool for managing Advent of Code 2025 solutions (12 days).

## Features

- Automatically download puzzle descriptions and inputs
- Generate Python template files for each day
- Test solutions with example inputs
- Run solutions with real inputs
- Submit answers directly from the command line
- Clean Markdown conversion of problem descriptions

## Setup

### 1. Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Session Cookie

The harness needs your Advent of Code session cookie to download inputs and submit answers.

#### How to Get Your Session Cookie:

1. Log in to [adventofcode.com](https://adventofcode.com)
2. Open Developer Tools (F12 or Right Click > Inspect)
3. Go to **Application** tab (Chrome) or **Storage** tab (Firefox)
4. Navigate to **Cookies** > `https://adventofcode.com`
5. Copy the value of the `session` cookie (long hexadecimal string)

#### Add to .env file:

```bash
cp .env.example .env
# Edit .env and paste your session cookie
```

Your `.env` file should look like:
```
AOC_SESSION=53616c7465645f5f...your_actual_cookie_here
```

**Important:** Keep your session cookie private! Don't commit `.env` to git.

## Usage

### Initialize a Day

Download problem descriptions and input for a specific day:

```bash
./aoc.py init day1
# or just:
./aoc.py init 1
# or use current day (if in December 1-12):
./aoc.py init
```

This creates:
```
day1/
├── step1.py          # Part 1 solution template
├── step2.py          # Part 2 solution template
├── step1.md          # Part 1 problem description
├── step2.md          # Part 2 problem description
├── test-input.txt    # Empty - add your test data here
└── input.txt         # Your puzzle input (downloaded)
```

### Test Your Solution

Run your solution with test input:

```bash
./aoc.py test day1
# or specify part:
./aoc.py test day1 -p 1
./aoc.py test day1 -p 2
```

### Run with Real Input

Run your solution with the actual puzzle input:

```bash
./aoc.py run day1
# or specify part:
./aoc.py run day1 -p 1
./aoc.py run day1 -p 2
```

### Submit Your Answer

Submit your answer to Advent of Code:

```bash
./aoc.py submit day1
# or specify part:
./aoc.py submit day1 -p 2
```

The tool will:
1. Run your solution to get the answer
2. Show you the answer and ask for confirmation
3. Submit it to Advent of Code
4. Display the result (correct, wrong, rate limited, etc.)

## Workflow Example

Here's a typical workflow for solving a day:

```bash
# 1. Initialize the day
./aoc.py init 1

# 2. Read the problem
cat day1/step1.md

# 3. Add test input from the problem description
# (Copy the example from step1.md and paste into test-input.txt)
nano day1/test-input.txt

# 4. Implement your solution
nano day1/step1.py

# 5. Test with example input
./aoc.py test 1

# 6. Run with real input
./aoc.py run 1

# 7. Submit when ready
./aoc.py submit 1
```

## Solution Template

Each `stepN.py` file is generated with this template:

```python
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
    # TODO: Implement solution
    pass

if __name__ == "__main__":
    import sys

    if '--test' in sys.argv:
        test_data = read_input('test-input.txt')
        test_result = solve(test_data)
        print(f"Test result: {test_result}")
    else:
        real_data = read_input('input.txt')
        result = solve(real_data)
        print(f"Result: {result}")
```

## Tips

- **Test First:** Always test with the example input before running with real input
- **Read Carefully:** AoC problems often have subtle details in the description
- **Check test-input.txt:** Make sure you've added the example input from the problem
- **Rate Limiting:** Wait at least 3 seconds between submissions (the tool enforces this)
- **Part 2:** Part 2 is only available after completing Part 1

## Troubleshooting

### "AOC_SESSION not found"
- Make sure you copied `.env.example` to `.env`
- Make sure you added your session cookie to `.env`

### "Day X input not yet available"
- The puzzle might not be released yet
- Check that today's date is in December 1-12, 2025
- The harness will create skeleton files you can use

### "Invalid session cookie"
- Your session cookie might have expired
- Log in to adventofcode.com again and get a new cookie
- Update your `.env` file

### Rate Limiting
- AoC has rate limits on submissions
- Wait a few minutes before submitting again
- The tool enforces a 3-second minimum between submissions

## Project Structure

```
aoc2025/
├── aoc.py              # Main CLI entry point
├── requirements.txt    # Python dependencies
├── .env                # Your session cookie (gitignored)
├── .env.example        # Template for .env
├── .gitignore          # Git ignore rules
├── README.md           # This file
├── lib/                # Support modules
│   ├── __init__.py
│   ├── aoc_client.py   # HTTP client for AoC API
│   ├── parser.py       # HTML to Markdown converter
│   ├── templates.py    # Template generator
│   └── utils.py        # Helper functions
└── dayN/               # One folder per day (created by init)
    ├── step1.py
    ├── step2.py
    ├── step1.md
    ├── step2.md
    ├── test-input.txt
    └── input.txt
```

## License

MIT License - feel free to modify and use as you like!

## Credits

Built for Advent of Code 2025 by Claude Code.

Happy coding! 🎄⭐
