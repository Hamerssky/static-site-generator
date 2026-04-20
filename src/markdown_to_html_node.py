from blocks import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import text_node_to_html_node, ParentNode, LeafNode
from text_to_textnode import text_to_textnode
from textnode import TextNode, TextType

def text_to_children(text):
    nodes = []
    for node in text_to_textnode(text):
        nodes.append(text_node_to_html_node(node))
    return nodes

def markdown_to_html_node(markdown):
    if not markdown:
        return ParentNode("div", [LeafNode(None, "")])

    parent = ParentNode("div", [])
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            cleaned = " ".join(block.split("\n"))
            node = ParentNode("p", text_to_children(cleaned))

        elif block_type == BlockType.HEADING:
            level = len(block) - len(block.lstrip("#"))
            level = level if level <= 6 else 6
            text = block[level:].strip()
            node = ParentNode(f"h{level}", text_to_children(text))

        elif block_type == BlockType.QUOTE:
            cleaned = " ".join(
                line.lstrip("> ").strip()
                for line in block.split("\n")
            )
            node = ParentNode("blockquote", text_to_children(cleaned))

        elif block_type == BlockType.UNORDERED_LIST:
            items = []
            for line in block.split("\n"):
                content = line[2:]
                items.append(ParentNode("li", text_to_children(content)))
            node = ParentNode("ul", items)

        elif block_type == BlockType.ORDERED_LIST:
            items = []
            for line in block.split("\n"):
                content = line.split(". ", 1)[1]
                items.append(ParentNode("li", text_to_children(content)))
            node = ParentNode("ol", items)

        elif block_type == BlockType.CODE:
            code_content = "\n".join(block.split("\n")[1:-1]) + "\n"
            node = ParentNode(
                "pre",
                [text_node_to_html_node(TextNode(code_content, TextType.CODE))]
            )

        else:
            raise ValueError("Invalid block type")

        parent.children.append(node) #type: ignore

    return parent
