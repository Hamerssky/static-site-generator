import unittest
from split_text import split_nodes_delimiter, split_nodes_link, split_nodes_image
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


class TestSplitNodesLinksImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_images_back_to_back(self):
        node = TextNode(
            "![a](url1)![b](url2)",
            TextType.TEXT,
        )
        result = split_nodes_image([node])

        self.assertEqual(result, [
            TextNode("a", TextType.IMAGE, "url1"),
            TextNode("b", TextType.IMAGE, "url2"),
        ])

    def test_image_at_start(self):
        node = TextNode(
            "![img](url) text after",
            TextType.TEXT,
        )
        result = split_nodes_image([node])

        self.assertEqual(result, [
            TextNode("img", TextType.IMAGE, "url"),
            TextNode(" text after", TextType.TEXT),
        ])

    def test_image_at_end(self):
        node = TextNode(
            "text before ![img](url)",
            TextType.TEXT,
        )
        result = split_nodes_image([node])

        self.assertEqual(result, [
            TextNode("text before ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url"),
        ])

    def test_no_images(self):
        node = TextNode("just text", TextType.TEXT)
        result = split_nodes_image([node])

        self.assertEqual(result, [node])

    def test_image_non_text_passthrough(self):
        node = TextNode("![img](url)", TextType.BOLD)
        result = split_nodes_image([node])

        self.assertEqual(result, [node])

    def test_multiple_links(self):
        node = TextNode(
            "a [one](url1) b [two](url2)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])

        self.assertEqual(result, [
            TextNode("a ", TextType.TEXT),
            TextNode("one", TextType.LINK, "url1"),
            TextNode(" b ", TextType.TEXT),
            TextNode("two", TextType.LINK, "url2"),
        ])

    def test_link_at_start(self):
        node = TextNode(
            "[link](url) rest",
            TextType.TEXT,
        )
        result = split_nodes_link([node])

        self.assertEqual(result, [
            TextNode("link", TextType.LINK, "url"),
            TextNode(" rest", TextType.TEXT),
        ])

    def test_link_at_end(self):
        node = TextNode(
            "before [link](url)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])

        self.assertEqual(result, [
            TextNode("before ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
        ])

    def test_no_links(self):
        node = TextNode("plain text", TextType.TEXT)
        result = split_nodes_link([node])

        self.assertEqual(result, [node])

    def test_image_not_link(self):
        node = TextNode("![img](url)", TextType.TEXT)
        result = split_nodes_link([node])

        self.assertEqual(result, [node])

    # Pipeline dependency, won't work unless processed in strict order images -> links
    def test_image_link_mix(self):
        node = TextNode("![text](url)[text](url)", TextType.TEXT)

        nodes = split_nodes_image([node])
        nodes = split_nodes_link(nodes)

        self.assertEqual(nodes, [
            TextNode("text", TextType.IMAGE, "url"),
            TextNode("text", TextType.LINK, "url"),
        ])

    def test_mixed_image_and_text(self):
        node = TextNode(
            "text ![img](url) more text",
            TextType.TEXT,
        )
        result = split_nodes_image([node])

        self.assertEqual(result, [
            TextNode("text ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url"),
            TextNode(" more text", TextType.TEXT),
        ])

if __name__ == "__main__":
    unittest.main()