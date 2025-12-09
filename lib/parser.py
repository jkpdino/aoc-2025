"""
HTML to Markdown parser for Advent of Code problems.
"""
from bs4 import BeautifulSoup
import html2text


class ProblemParser:
    """Parser for converting AoC problem HTML to Markdown."""

    def __init__(self):
        """Initialize the HTML to Markdown converter."""
        self.html_converter = html2text.HTML2Text()
        self.html_converter.body_width = 0  # Don't wrap lines
        self.html_converter.ignore_links = False  # Preserve links
        self.html_converter.ignore_images = False  # Preserve images
        self.html_converter.ignore_emphasis = False  # Keep bold/italic

    def parse_problem(self, html_content):
        """
        Extract problem descriptions from HTML.

        Args:
            html_content: Full HTML page content

        Returns:
            list: List of markdown strings [part1] or [part1, part2]
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = soup.find_all('article', class_='day-desc')

        parts = []
        for article in articles:
            markdown = self.html_converter.handle(str(article))
            cleaned = self._clean_markdown(markdown)
            parts.append(cleaned)

        return parts

    def _clean_markdown(self, markdown):
        """
        Clean up markdown formatting.

        Args:
            markdown: Raw markdown string

        Returns:
            str: Cleaned markdown
        """
        lines = markdown.split('\n')
        cleaned_lines = []
        prev_blank = False

        for line in lines:
            is_blank = line.strip() == ''
            # Remove excessive blank lines (more than 1 consecutive)
            if not (is_blank and prev_blank):
                cleaned_lines.append(line)
            prev_blank = is_blank

        return '\n'.join(cleaned_lines).strip()
