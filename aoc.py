#!/usr/bin/env python3
"""
Advent of Code 2025 Test Harness

CLI tool for managing Advent of Code solutions.
"""
import argparse
import os
import sys
import subprocess
from bs4 import BeautifulSoup
import requests

from lib.utils import (
    get_current_day, validate_day, load_session_cookie,
    parse_day_arg, ensure_directory
)
from lib.aoc_client import AoCClient
from lib.parser import ProblemParser
from lib.templates import generate_step_template


def cmd_init(args):
    """Initialize a day's folder structure."""
    try:
        day = parse_day_arg(args.day)
        day = validate_day(day)

        day_dir = f"day{day}"

        # Check if directory exists
        if os.path.exists(day_dir):
            response = input(f"{day_dir} already exists. Overwrite? (y/n): ")
            if response.lower() != 'y':
                print("Cancelled.")
                return

        print(f"Initializing Day {day}...")

        # Create directory
        ensure_directory(day_dir)

        # Generate step templates
        print("Creating step1.py and step2.py...")
        with open(f"{day_dir}/step1.py", 'w') as f:
            f.write(generate_step_template(day, 1))
        with open(f"{day_dir}/step2.py", 'w') as f:
            f.write(generate_step_template(day, 2))

        # Create empty test-input.txt
        print("Creating test-input.txt...")
        with open(f"{day_dir}/test-input.txt", 'w') as f:
            f.write("")

        # Download problem and input
        try:
            session = load_session_cookie()
            client = AoCClient(session)
            parser = ProblemParser()

            # Download problem description
            print(f"Downloading problem description...")
            try:
                html = client.download_problem(day)
                parts = parser.parse_problem(html)

                if len(parts) >= 1:
                    with open(f"{day_dir}/step1.md", 'w') as f:
                        f.write(parts[0])
                    print("  step1.md created")

                if len(parts) >= 2:
                    with open(f"{day_dir}/step2.md", 'w') as f:
                        f.write(parts[1])
                    print("  step2.md created")
                elif len(parts) == 1:
                    print("  step2.md not available yet (complete Part 1 first)")
                    # Create placeholder
                    with open(f"{day_dir}/step2.md", 'w') as f:
                        f.write("# Part 2\n\nComplete Part 1 first to unlock Part 2.")
            except requests.HTTPError as e:
                if e.response.status_code == 404:
                    print(f"  Warning: Day {day} problem not yet available")
                    # Create placeholders
                    for part in [1, 2]:
                        with open(f"{day_dir}/step{part}.md", 'w') as f:
                            f.write(f"# Day {day} Part {part}\n\nProblem not yet available.")
                else:
                    raise

            # Download input
            print("Downloading input...")
            try:
                input_text = client.download_input(day)
                with open(f"{day_dir}/input.txt", 'w') as f:
                    f.write(input_text)
                print("  input.txt downloaded")
            except requests.HTTPError as e:
                if e.response.status_code == 404:
                    print(f"  Warning: Day {day} input not yet available")
                    with open(f"{day_dir}/input.txt", 'w') as f:
                        f.write("")
                else:
                    raise

        except ValueError as e:
            print(f"Warning: {e}")
            print("Creating skeleton files only.")
            # Create placeholder files
            for part in [1, 2]:
                with open(f"{day_dir}/step{part}.md", 'w') as f:
                    f.write(f"# Day {day} Part {part}\n\nProblem description goes here.")
            with open(f"{day_dir}/input.txt", 'w') as f:
                f.write("")

        print(f"\nDay {day} initialized successfully!")
        print(f"\nNext steps:")
        print(f"  1. Read the problem: {day_dir}/step1.md")
        print(f"  2. Add test input: {day_dir}/test-input.txt")
        print(f"  3. Implement solution: {day_dir}/step1.py")
        print(f"  4. Test: ./aoc.py test {day}")
        print(f"  5. Run: ./aoc.py run {day}")

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except requests.RequestException as e:
        print(f"Network error: {e}")
        print("Tip: Check your internet connection and session cookie")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


def cmd_test(args):
    """Run solution with test input."""
    try:
        day = parse_day_arg(args.day)
        day = validate_day(day)

        # Get part number
        part = args.part if args.part else 1
        if part not in [1, 2]:
            print("Error: Part must be 1 or 2")
            sys.exit(1)

        day_dir = f"day{day}"
        script_path = f"{day_dir}/step{part}.py"

        if not os.path.exists(script_path):
            print(f"Error: {script_path} not found.")
            print(f"Run './aoc.py init {day}' first.")
            sys.exit(1)

        print(f"Running Day {day} Part {part} with test input...\n")
        result = subprocess.run(
            [sys.executable, f"step{part}.py", "--test"],
            cwd=day_dir
        )
        sys.exit(result.returncode)

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


def cmd_run(args):
    """Run solution with real input."""
    try:
        day = parse_day_arg(args.day)
        day = validate_day(day)

        # Get part number
        part = args.part if args.part else 1
        if part not in [1, 2]:
            print("Error: Part must be 1 or 2")
            sys.exit(1)

        day_dir = f"day{day}"
        script_path = f"{day_dir}/step{part}.py"

        if not os.path.exists(script_path):
            print(f"Error: {script_path} not found.")
            print(f"Run './aoc.py init {day}' first.")
            sys.exit(1)

        print(f"Running Day {day} Part {part} with real input...\n")
        result = subprocess.run(
            [sys.executable, f"step{part}.py"],
            cwd=day_dir
        )
        sys.exit(result.returncode)

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


def cmd_submit(args):
    """Submit solution answer."""
    try:
        day = parse_day_arg(args.day)
        day = validate_day(day)

        # Get part number
        if args.part:
            part = args.part
        else:
            part = int(input("Which part to submit? (1 or 2): "))

        if part not in [1, 2]:
            print("Error: Part must be 1 or 2")
            sys.exit(1)

        day_dir = f"day{day}"
        script_path = f"{day_dir}/step{part}.py"

        if not os.path.exists(script_path):
            print(f"Error: {script_path} not found.")
            print(f"Run './aoc.py init {day}' first.")
            sys.exit(1)

        # Run solution to get answer
        print(f"Running Day {day} Part {part} to get answer...\n")
        result = subprocess.run(
            [sys.executable, f"step{part}.py"],
            cwd=day_dir,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print("Error: Solution failed to run")
            print(result.stderr)
            sys.exit(1)

        # Parse output to get answer
        output = result.stdout.strip()
        print(output)
        print()

        # Extract answer from output (look for last line with "Result:")
        answer = None
        for line in output.split('\n'):
            if 'Result:' in line:
                answer = line.split('Result:')[-1].strip()

        if not answer or answer == 'None':
            print("Error: Could not extract answer from solution output")
            print("Make sure your solution prints 'Result: <answer>'")
            sys.exit(1)

        # Confirm submission
        response = input(f"\nSubmit answer '{answer}' for Day {day} Part {part}? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return

        # Submit
        session = load_session_cookie()
        client = AoCClient(session)

        print("Submitting...")
        response_html = client.submit_answer(day, part, answer)

        # Parse response
        result_msg = parse_submission_response(response_html)
        print(f"\n{result_msg}")

        # If successful and part 1, download step2
        if "SUCCESS" in result_msg and part == 1:
            print("\nDownloading Part 2...")
            try:
                parser = ProblemParser()
                html = client.download_problem(day)
                parts = parser.parse_problem(html)

                if len(parts) >= 2:
                    with open(f"{day_dir}/step2.md", 'w') as f:
                        f.write(parts[1])
                    print(f"✓ Part 2 description saved to {day_dir}/step2.md")
                else:
                    print("✗ Part 2 not yet available (try again in a moment)")
            except Exception as e:
                print(f"Warning: Could not download Part 2: {e}")
                print("You can manually run './aoc.py init {day}' to download it later")

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except requests.RequestException as e:
        print(f"Network error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(1)


def parse_submission_response(html):
    """
    Parse submission response to determine success/failure.

    Args:
        html: Response HTML

    Returns:
        str: Formatted result message
    """
    soup = BeautifulSoup(html, 'html.parser')
    article = soup.find('article')
    if not article:
        return "Unknown response - check website"

    text = article.get_text().strip()

    if "That's the right answer" in text:
        return "SUCCESS: Correct answer! ⭐"
    elif "not the right answer" in text:
        if "too high" in text:
            return "WRONG: Answer is too high"
        elif "too low" in text:
            return "WRONG: Answer is too low"
        return "WRONG: Incorrect answer"
    elif "gave an answer too recently" in text:
        return "RATE LIMITED: Please wait before submitting again"
    elif "don't seem to be solving the right level" in text:
        return "ERROR: Already completed or wrong part"

    return f"UNKNOWN RESPONSE:\n{text[:300]}"


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Advent of Code 2025 Test Harness",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # init command
    parser_init = subparsers.add_parser('init', help='Initialize a day')
    parser_init.add_argument('day', nargs='?', help='Day number (e.g., 1 or day1)')

    # test command
    parser_test = subparsers.add_parser('test', help='Run with test input')
    parser_test.add_argument('day', nargs='?', help='Day number (e.g., 1 or day1)')
    parser_test.add_argument('-p', '--part', type=int, choices=[1, 2], help='Part number')

    # run command
    parser_run = subparsers.add_parser('run', help='Run with real input')
    parser_run.add_argument('day', nargs='?', help='Day number (e.g., 1 or day1)')
    parser_run.add_argument('-p', '--part', type=int, choices=[1, 2], help='Part number')

    # submit command
    parser_submit = subparsers.add_parser('submit', help='Submit answer')
    parser_submit.add_argument('day', nargs='?', help='Day number (e.g., 1 or day1)')
    parser_submit.add_argument('-p', '--part', type=int, choices=[1, 2], help='Part number')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Route to command handlers
    if args.command == 'init':
        cmd_init(args)
    elif args.command == 'test':
        cmd_test(args)
    elif args.command == 'run':
        cmd_run(args)
    elif args.command == 'submit':
        cmd_submit(args)


if __name__ == "__main__":
    main()
