import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()