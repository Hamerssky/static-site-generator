import unittest

from htmlnode import HTMLNode, LeafNode


class TestTextNode(unittest.TestCase):
    def test_htmlnode(self):
        node = HTMLNode("a", "YouTube", None, {"href": "www.youtube.com", "target": "_blank"})
        node2 = HTMLNode(None, " has amazing videos!")
        node3 = HTMLNode("h1", None, [node, node2])

        print(node)
        print(node2)
        print(node3)

        self.assertEqual(node.props_to_html(), " href=\"www.youtube.com\" target=\"_blank\"")
        self.assertEqual(node2.props_to_html(), "")
        self.assertEqual(node3.children, [node, node2])

    def test_leaf_to_html(self):
        node = LeafNode(None, "Hello, world!")
        node2 = LeafNode("", "Hello, world!")

        self.assertEqual(node.to_html(), "Hello, world!")
        self.assertEqual(node2.to_html(), "Hello, world!")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("p", "This is a paragraph of text.")

        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node2.to_html(), "<p>This is a paragraph of text.</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

    def test_leaf_to_html_span(self):
        node = LeafNode("span", "This text is red!", {"style": "color: red;"})

        self.assertEqual(node.to_html(), "<span style=\"color: red;\">This text is red!</span>")

if __name__ == "__main__":
    unittest.main()