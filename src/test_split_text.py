import unittest
from split_text import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_basic_bold(self):
        nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)

        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ])

    def test_multiple_bold_sections(self):
        nodes = [TextNode("**bold1** and **bold2**", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)

        self.assertEqual(result, [
            TextNode("bold1", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold2", TextType.BOLD),
        ])

    def test_no_delimiter(self):
        nodes = [TextNode("plain text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)

        self.assertEqual(result, [
            TextNode("plain text", TextType.TEXT)
        ])

    def test_non_text_node_passthrough(self):
        nodes = [TextNode("bold", TextType.BOLD)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)

        self.assertEqual(result, nodes)

    def test_unmatched_delimiter_raises(self):
        nodes = [TextNode("This is **broken text", TextType.TEXT)]

        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, "**", TextType.BOLD)

    def test_empty_string(self):
        nodes = [TextNode("", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)

        self.assertEqual(result, [])

    def test_only_delimiters(self):
        nodes = [TextNode("****", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)

        self.assertEqual(result, [])
