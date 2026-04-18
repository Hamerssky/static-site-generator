import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
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

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node2 = LeafNode("i", "grandchild2")
        grandchild_node3 = LeafNode("a", "grandchild3", {"href": "www.youtube.com"})
        child_node = ParentNode("span", [grandchild_node, grandchild_node2])
        child_node2 = ParentNode("span", [grandchild_node3])
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b><i>grandchild2</i></span><span><a href=\"www.youtube.com\">grandchild3</a></span></div>"
        )

if __name__ == "__main__":
    unittest.main()