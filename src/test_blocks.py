import unittest

from blocks import markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_input(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_whitespace_only(self):
        md = "\n\n   \n\n"
        self.assertEqual(markdown_to_blocks(md), [])

    def test_single_block(self):
        md = "just text"
        self.assertEqual(markdown_to_blocks(md), ["just text"])

    def test_multiple_blank_lines(self):
        md = "a\n\n\n\nb"
        self.assertEqual(markdown_to_blocks(md), ["a", "b"])

    def test_strip_blocks(self):
        md = "  a  \n\n  b  "
        self.assertEqual(markdown_to_blocks(md), ["a", "b"])

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(
            block_to_block_type("# Heading"),
            BlockType.HEADING
        )

    def test_heading_multiple_hashes(self):
        self.assertEqual(
            block_to_block_type("### Heading"),
            BlockType.HEADING
        )

    def test_code_block(self):
        block = "```\ncode here\n```"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE
        )

    def test_quote(self):
        block = "> line one\n>line two"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE
        )

    def test_unordered_list(self):
        block = "- item one\n- item two"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST
        )

    def test_ordered_list(self):
        block = "1. one\n2. two\n3. three"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST
        )

    def test_paragraph(self):
        self.assertEqual(
            block_to_block_type("just text"),
            BlockType.PARAGRAPH
        )

    def test_mixed_block_is_paragraph(self):
        block = "text\n- not really a list"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

    def test_invalid_quote(self):
        block = "> valid\nnot quote"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

    def test_invalid_unordered_list(self):
        block = "- item\nnot item"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

    def test_invalid_ordered_list(self):
        block = "1. one\n3. three"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

if __name__ == "__main__":
    unittest.main()