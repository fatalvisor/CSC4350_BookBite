import unittest
from unittest.mock import MagicMock, patch
from penguin import tag_remove, get_themes, get_single_book_theme, title_search


class HtmlTagRemovalTests(unittest.TestCase):
    """Houses a couple of tests for Penguin.py's tag_remove() function."""

    def test_html_string(self):
        """Checks if HTML tags are being removed properly."""
        test_string = "<h1>Testing... 1, 2, 3</h1>"
        expected_output = "Testing... 1, 2, 3"
        function_output = tag_remove(test_string)
        self.assertEqual(expected_output, function_output)

    def test_normal_string(self):
        """Checks if no errors are being thrown when a normal string without HTML tags is checked."""
        test_string = "Nice to meet you. My favorite html tag is h1."
        expected_output = "Nice to meet you. My favorite html tag is h1."
        function_output = tag_remove(test_string)
        self.assertEqual(expected_output, function_output)


class ThemeListTests(unittest.TestCase):
    """Houses a couple of tests for Penguin.py's get_themes() function."""

    def test_themelist_to_string(self):
        """Checks if a list of themes are properly displayed in a single sentence."""
        test_themes = {"theme": ["Friendship", "Horror", "Thriller", "Adventure"]}
        expected_output = "Themes: Friendship, Horror, Thriller, Adventure"
        function_output = get_themes(test_themes)
        self.assertEqual(expected_output, function_output)

    def test_no_themes(self):
        """Checks if no errors are being thrown if a book was not classified under any theme."""
        test_theme = None
        expected_output = "None"
        function_output = get_themes(test_theme)
        self.assertEqual(expected_output, function_output)


class PenguinTests(unittest.TestCase):
    "Houses a couple of tests involving Penguin's major info-grabbing functions."

    def test_specific_book_theme(self):
        """Checks if a single theme is being returned, assuming a book only has one theme."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "themes": {"theme": ["Coming of Age", "Fantasy", "War"]}
        }

        with patch("penguin.requests.get") as mock_get:
            mock_get.return_value = mock_response
            self.assertEqual(get_single_book_theme(123456789123), "Coming of Age")

    def test_title_search(self):
        """Checks if a single theme is being returned, assuming a book only has one theme."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"title": [{"isbn": 1234567890}]}

        with patch("penguin.requests.get") as mock_get:
            mock_get.return_value = mock_response
            self.assertEqual(title_search("Sample Title"), 1234567890)


if __name__ == "__main__":
    unittest.main()
