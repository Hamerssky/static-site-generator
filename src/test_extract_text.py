import unittest

from extract_text import extract_markdown_images, extract_markdown_links


class TestExtractText(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](www.example.com)"
        )
        self.assertListEqual([("link", "www.example.com")], matches)

    def test_extract_markdown_images_ex_links(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png). This is text with a [link](www.example.com)."
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links_ex_images(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png). This is text with a [link](www.example.com)."
        )
        self.assertListEqual([("link", "www.example.com")], matches)

    def test_extract_markdown_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](www.example.com). This is text with a [link2](www.example2.com)."
        )
        self.assertListEqual([("link", "www.example.com"), ("link2", "www.example2.com")], matches) 

if __name__ == "__main__":
    unittest.main()