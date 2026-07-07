from textnode import TextNode, TextType
import re


def text_to_textnodes(text: str) -> list[TextNode, TextNode]:
    node = [TextNode(text, TextType.TEXT)]
    bold_nodes = split_nodes_delimiter(node, "**", TextType.BOLD)
    italic_nodes = split_nodes_delimiter(bold_nodes, "_", TextType.ITALIC)
    code_nodes = split_nodes_delimiter(italic_nodes, "`", TextType.CODE)
    img_nodes = split_nodes_image(code_nodes)
    link_node = split_nodes_link(img_nodes)
    return link_node

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))        
        new_nodes.extend(split_nodes)    
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        images = extract_markdown_images(old_node.text)
        if images == []:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        remaining_text = old_node.text
        for image in images:
            parts = remaining_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(parts) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if parts[0] != "":
                split_nodes.append(TextNode(parts[0], TextType.TEXT))
            split_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            remaining_text = parts[1]
        if remaining_text != "":
            split_nodes.append(TextNode(remaining_text, TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes
            

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)
        if links == []:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        remaining_text = old_node.text
        for link in links:
            parts = remaining_text.split(f"[{link[0]}]({link[1]})", 1)
            if parts[0] != "":
                split_nodes.append(TextNode(parts[0], TextType.TEXT))
            split_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            remaining_text = parts[1]
        if remaining_text != "":
            split_nodes.append(TextNode(remaining_text, TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches