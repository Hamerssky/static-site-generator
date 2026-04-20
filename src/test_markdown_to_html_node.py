import unittest
from markdown_to_html_node import markdown_to_html_node

class TestMarkdownToHTMKNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_paragraph_simple(self):
        md = "just text"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><p>just text</p></div>")

    def test_paragraph_multiline(self):
        md = "line one\nline two\nline three"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><p>line one line two line three</p></div>")

    def test_multiple_paragraphs(self):
        md = "first\n\nsecond"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><p>first</p><p>second</p></div>")

    def test_heading(self):
        md = "# Heading"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><h1>Heading</h1></div>")

    def test_heading_levels(self):
        md = "### Heading 3"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><h3>Heading 3</h3></div>")

    def test_quote(self):
        md = "> quote line one\n> quote line two"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><blockquote>quote line one quote line two</blockquote></div>"
        )

    def test_unordered_list(self):
        md = "- one\n- two\n- three"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ul><li>one</li><li>two</li><li>three</li></ul></div>"
        )

    def test_ordered_list(self):
        md = "1. one\n2. two\n3. three"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ol><li>one</li><li>two</li><li>three</li></ol></div>"
        )

    def test_code_block(self):
        md = "```\ncode here\nmore code\n```"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><pre><code>code here\nmore code\n</code></pre></div>"
        )

    def test_inline_formatting(self):
        md = "this is **bold** and _italic_ and `code`"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><p>this is <b>bold</b> and <i>italic</i> and <code>code</code></p></div>"
        )

    def test_links_and_images(self):
        md = "![img](url)[link](url)"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            '<div><p><img src="url" alt="img"></img><a href="url">link</a></p></div>'
        )

    def test_mixed_everything(self):
        md = """
# Title

This is **bold** text and _italic_

- item one
- item two

> quoted text

1. first
2. second
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div>"
            "<h1>Title</h1>"
            "<p>This is <b>bold</b> text and <i>italic</i></p>"
            "<ul><li>item one</li><li>item two</li></ul>"
            "<blockquote>quoted text</blockquote>"
            "<ol><li>first</li><li>second</li></ol>"
            "</div>"
        )

    def test_code_block_ignores_inline(self):
        md = "```\nthis is **not bold**\n```"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><pre><code>this is **not bold**\n</code></pre></div>"
        )

    def test_empty_input(self):
        md = ""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div></div>")

if __name__ == "__main__":
    unittest.main()