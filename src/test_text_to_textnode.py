import unittest

from textnode import TextNode, TextType
from text_to_textnode import text_to_textnode


class TestTextToTextNode(unittest.TestCase):
    def test_plain_text(self):
        result = text_to_textnode("just text")

        self.assertEqual(result, [
            TextNode("just text", TextType.TEXT)
        ])

    def test_bold(self):
        result = text_to_textnode("this is **bold** text")

        self.assertEqual(result, [
            TextNode("this is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ])

    def test_italic(self):
        result = text_to_textnode("this is _italic_ text")

        self.assertEqual(result, [
            TextNode("this is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ])

    def test_code(self):
        result = text_to_textnode("this is `code` text")

        self.assertEqual(result, [
            TextNode("this is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ])

    def test_image(self):
        result = text_to_textnode("image ![alt](url) here")

        self.assertEqual(result, [
            TextNode("image ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode(" here", TextType.TEXT),
        ])

    def test_link(self):
        result = text_to_textnode("go to [site](url) now")

        self.assertEqual(result, [
            TextNode("go to ", TextType.TEXT),
            TextNode("site", TextType.LINK, "url"),
            TextNode(" now", TextType.TEXT),
        ])

    def test_image_and_link(self):
        result = text_to_textnode("![img](url)[link](url)")

        self.assertEqual(result, [
            TextNode("img", TextType.IMAGE, "url"),
            TextNode("link", TextType.LINK, "url"),
        ])

    def test_bold_inside_text(self):
        result = text_to_textnode("a **bold** and _italic_")

        self.assertEqual(result, [
            TextNode("a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ])

    def test_all_types_mixed(self):
        result = text_to_textnode(
            "Start **bold** _italic_ `code` [link](url) ![img](url)"
        )

        self.assertEqual(result, [
            TextNode("Start ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode(" ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url"),
        ])

    def test_image_then_link_order(self):
        result = text_to_textnode("![a](url)[b](url)")

        self.assertEqual(result, [
            TextNode("a", TextType.IMAGE, "url"),
            TextNode("b", TextType.LINK, "url"),
        ])

    def test_back_to_back_formatting(self):
        result = text_to_textnode("**a**_b_`c`")

        self.assertEqual(result, [
            TextNode("a", TextType.BOLD),
            TextNode("b", TextType.ITALIC),
            TextNode("c", TextType.CODE),
        ])

    def test_starts_with_format(self):
        result = text_to_textnode("**bold** text")

        self.assertEqual(result, [
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ])

    def test_ends_with_format(self):
        result = text_to_textnode("text **bold**")

        self.assertEqual(result, [
            TextNode("text ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ])

    def test_unclosed_bold(self):
        with self.assertRaises(Exception):
            text_to_textnode("this is **broken")

if __name__ == "__main__":
    unittest.main()