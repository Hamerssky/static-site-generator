from textnode import TextNode, TextType

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