import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.ITALIC)
        node4 = TextNode("This is a text node", TextType.BOLD, "www.youtube.com")
        node5 = TextNode("This is a text node", TextType.BOLD, "www.wikipedia.com")
        node6 = TextNode("This is a text node", TextType.BOLD, "www.wikipedia.com")

        self.assertEqual(node, node2)
        self.assertNotEqual(node2, node3)
        self.assertNotEqual(node2, node4)
        self.assertNotEqual(node4, node5)
        self.assertEqual(node5, node6)


if __name__ == "__main__":
    unittest.main()