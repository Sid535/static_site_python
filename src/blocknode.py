import re
from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown) -> list[str, str]:
    new_blocks = []
    split_blocks = re.split(r"\n\s*\n", markdown.strip())
    for block in split_blocks:
        block = block.strip()
        if block != "":
            new_blocks.append(block)
    return new_blocks


def block_to_block_type(markdown_block) -> BlockType:
    lines = markdown_block.split("\n")
    if re.match(r"^#{1,6} ", markdown_block):
        return BlockType.HEADING
    elif markdown_block.startswith("```\n") and markdown_block.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    elif all(line.startswith(f"{i + 1}. ") for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
    
def text_to_children(text: str) -> HTMLNode:
    leaf_nodes_list = []
    test_nodes = text_to_textnodes(text)
    for text_node in test_nodes:
        leaf_node = text_node_to_html_node(text_node)
        leaf_nodes_list.append(leaf_node)
    return leaf_nodes_list

def block_to_html_node(block: str, block_type: BlockType) -> HTMLNode:
    lines = block.splitlines()
    match block_type:
        case BlockType.HEADING:
            count = 0
            for char in block:
                if char == "#":
                    count += 1
                    continue
                break
            block = block[count+1:]
            tag = f"h{count}"
            children = text_to_children(block)
            return ParentNode(tag, children)
        case BlockType.CODE:
            lines = lines[1:-1]
            block = "\n".join(lines)
            block += "\n"
            children = text_node_to_html_node(TextNode(block, TextType.CODE))
            return ParentNode("pre", [children])
        case BlockType.QUOTE:
            cleaned_line = []
            for line in lines:
                line = line[1:].strip()
                cleaned_line.append(line)
            block = " ".join(cleaned_line)
            children = text_to_children(block)
            return ParentNode("blockquote", children)
        case BlockType.UNORDERED_LIST:
            parent = []
            for line in lines:
                line = line[2:]
                children = []
                children.extend(text_to_children(line))
                parent.append(ParentNode("li", children))
            return ParentNode("ul", parent)
        case BlockType.ORDERED_LIST:
            parent = []
            for line in lines:
                count = 0
                for char in line:
                    if char.isdigit():
                        count += 1
                        continue
                    break
                line = line[count+2:]
                children = []
                children.extend(text_to_children(line))
                parent.append(ParentNode("li", children))
            return ParentNode("ol", parent)
        case _:
            block = block.replace("\n", " ")
            children = text_to_children(block)
            return ParentNode("p", children)
        
    
    
def markdown_to_html_node(markdown) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    child_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block = block_to_html_node(block, block_type)
        child_nodes.append(block)
    
    parent_node = ParentNode("div", child_nodes)
    return parent_node