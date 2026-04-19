from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str):
    blocks = []
    for block in markdown.split("\n\n"):
        block = block.strip()
        if block == "":
            continue
        blocks.append(block)
    return blocks

def block_to_block_type(block: str):
    if not block:
        return None

    # Heading block
    if block.startswith("#"):
        level = 1

        while len(block) > level and block[level] == "#" and level < 6:
            level += 1
        
        return BlockType.HEADING
    
    # Code block
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    # Quote block
    is_quote = True

    for line in block.split("\n"):
        if not line:
            is_quote = False
            break
        if not line.startswith(">"):
            is_quote = False
            break

    if is_quote:
        return BlockType.QUOTE
    
    # Unordered list
    is_unordered_list = True

    for line in block.split("\n"):
        if not line:
            is_unordered_list = False
            break
        if not line.startswith("- "):
            is_unordered_list = False
            break

    if is_unordered_list:
        return BlockType.UNORDERED_LIST
    
    # Ordered list
    lines = block.split("\n")

    first_match = re.match(r"(\d+)\. ", lines[0])
    if not first_match:
        return BlockType.PARAGRAPH

    expected = int(first_match.group(1))

    for line in lines:
        match = re.match(r"(\d+)\. ", line)
        if not match:
            return BlockType.PARAGRAPH

        number = int(match.group(1))
        if number != expected:
            return BlockType.PARAGRAPH

        expected += 1

    return BlockType.ORDERED_LIST

