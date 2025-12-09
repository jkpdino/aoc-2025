"""
Utility functions for Advent of Code test harness.
"""
from datetime import datetime
from dotenv import load_dotenv
import os


def get_current_day():
    """
    Get current AoC day (1-12) based on today's date.

    Returns:
        int: Current day number (1-12)

    Raises:
        ValueError: If not in December or if day > 12
    """
    today = datetime.now()
    if today.month != 12:
        raise ValueError("Advent of Code only runs in December!")
    day = today.day
    if day > 12:
        day = 12  # Cap at 12 for this custom harness
    return day


def validate_day(day):
    """
    Validate day is between 1 and 12.

    Args:
        day: Day number to validate

    Returns:
        int: Validated day number

    Raises:
        ValueError: If day is not between 1 and 12
    """
    if not (1 <= day <= 12):
        raise ValueError(f"Day must be between 1 and 12, got {day}")
    return day


def load_session_cookie():
    """
    Load AOC_SESSION from .env file.

    Returns:
        str: Session cookie value

    Raises:
        ValueError: If AOC_SESSION not found in .env
    """
    load_dotenv()
    session = os.getenv('AOC_SESSION')
    if not session:
        raise ValueError(
            "AOC_SESSION not found in .env file.\n"
            "Copy .env.example to .env and add your session cookie.\n"
            "See README.md for instructions on getting your session cookie."
        )
    return session


def parse_day_arg(day_str):
    """
    Parse day argument: 'day1' or '1' -> 1, None -> current day.

    Args:
        day_str: Day argument string or None

    Returns:
        int: Parsed day number

    Raises:
        ValueError: If day_str has invalid format
    """
    if day_str is None:
        return get_current_day()

    # Remove 'day' prefix if present
    day_str = day_str.lower().replace('day', '')
    try:
        return int(day_str)
    except ValueError:
        raise ValueError(f"Invalid day format: {day_str}. Use 'day1' or '1'")


def ensure_directory(path):
    """
    Create directory if it doesn't exist.

    Args:
        path: Directory path to create
    """
    os.makedirs(path, exist_ok=True)
