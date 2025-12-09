"""
HTTP client for Advent of Code API.
"""
import requests
from time import time, sleep


class AoCClient:
    """Client for interacting with Advent of Code API."""

    BASE_URL = "https://adventofcode.com/2025"
    RATE_LIMIT_SECONDS = 3

    def __init__(self, session_cookie):
        """
        Initialize AoC client with session cookie.

        Args:
            session_cookie: Session cookie value from browser
        """
        self.session = requests.Session()
        self.session.cookies.set('session', session_cookie)
        self.last_submission_time = 0

    def download_input(self, day):
        """
        Download puzzle input for a given day.

        Args:
            day: Day number (1-12)

        Returns:
            str: Puzzle input text

        Raises:
            requests.HTTPError: If download fails
        """
        url = f"{self.BASE_URL}/day/{day}/input"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.text

    def download_problem(self, day):
        """
        Download problem description HTML for a given day.

        Args:
            day: Day number (1-12)

        Returns:
            str: Problem page HTML

        Raises:
            requests.HTTPError: If download fails
        """
        url = f"{self.BASE_URL}/day/{day}"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.text

    def submit_answer(self, day, part, answer):
        """
        Submit an answer for a given day and part.

        Args:
            day: Day number (1-12)
            part: Part number (1 or 2)
            answer: Answer to submit

        Returns:
            str: Response HTML

        Raises:
            requests.HTTPError: If submission fails
        """
        # Rate limiting
        elapsed = time() - self.last_submission_time
        if elapsed < self.RATE_LIMIT_SECONDS:
            wait_time = self.RATE_LIMIT_SECONDS - elapsed
            print(f"Rate limiting: waiting {wait_time:.1f} seconds...")
            sleep(wait_time)

        url = f"{self.BASE_URL}/day/{day}/answer"
        data = {'level': str(part), 'answer': str(answer)}
        response = self.session.post(
            url,
            data=data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=30
        )
        self.last_submission_time = time()
        response.raise_for_status()
        return response.text
