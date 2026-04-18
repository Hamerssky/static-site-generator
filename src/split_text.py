from textnode import TextNode, TextType
from extract_text import extract_markdown_links, extract_markdown_images

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # TODO: Add support for multiple delimeters in one text 
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception(f"Invalid markdown syntax - missing closing delimeter: {delimiter}")
        for i, new_node in enumerate(parts):
            if new_node == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(new_node, TextType.TEXT))
            else:
                new_nodes.append(TextNode(new_node, text_type))

    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        remaining = node.text
        images = extract_markdown_images(remaining)

        for alt, url in images:
            before, remaining = remaining.split(f"![{alt}]({url})", 1)

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, url))

        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes: list[TextNode] = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        remaining = node.text
        links = extract_markdown_links(remaining)

        for text, url in links:
            before, remaining = remaining.split(f"[{text}]({url})", 1)

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(text, TextType.LINK, url))

        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes
