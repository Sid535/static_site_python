import unittest
from generate_page import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_basic_h1(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_h1_with_extra_whitespace(self):
        self.assertEqual(extract_title("#    Hello World   "), "Hello World")

    def test_h1_among_other_lines(self):
        md = "Some intro text\n# My Title\nMore content here"
        self.assertEqual(extract_title(md), "My Title")

    def test_h1_not_on_first_line(self):
        md = "## Subheading\n# Real Title\nBody text"
        self.assertEqual(extract_title(md), "Real Title")

    def test_ignores_h2_and_deeper(self):
        md = "## Not this one\n### Also not this\n# The Title"
        self.assertEqual(extract_title(md), "The Title")

    def test_no_header_raises(self):
        md = "Just some text\nwith no headers\nat all"
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_empty_string_raises(self):
        with self.assertRaises(ValueError):
            extract_title("")

    def test_hash_with_no_space_is_not_h1(self):
        md = "#Hello\nSome text"
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_bare_hash_returns_empty_title(self):
        self.assertEqual(extract_title("#"), "")

    def test_multiple_h1s_returns_first(self):
        md = "# First Title\n# Second Title"
        self.assertEqual(extract_title(md), "First Title")


if __name__ == "__main__":
    unittest.main()