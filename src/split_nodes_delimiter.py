import re

from textnode import TextNode, InlineTextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != InlineTextType.PLAIN:
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
                split_nodes.append(TextNode(sections[i], InlineTextType.PLAIN))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != InlineTextType.PLAIN:
            new_nodes.append(old_node)
            continue
        
        images = extract_markdown_images(old_node.text)
        
        if not images:
            new_nodes.append(old_node)
            continue
        
        remaining_text = old_node.text
        for alt_text, url in images:
            sections = remaining_text.split(f"![{alt_text}]({url})", 1)
            
            if sections[0]:
                new_nodes.append(TextNode(sections[0], InlineTextType.PLAIN))
            
            new_nodes.append(TextNode(alt_text, InlineTextType.IMAGE, url))
            
            remaining_text = sections[1] if len(sections) > 1 else ""
        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, InlineTextType.PLAIN))
    
    return new_nodes


def split_nodes_link(old_nodes):
    
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != InlineTextType.PLAIN:
            new_nodes.append(old_node)
            continue
        
        links = extract_markdown_links(old_node.text)
        
        if not links:
            new_nodes.append(old_node)
            continue
        
        remaining_text = old_node.text
        for anchor_text, url in links:
            sections = remaining_text.split(f"[{anchor_text}]({url})", 1)
            
            if sections[0]:
                new_nodes.append(TextNode(sections[0], InlineTextType.PLAIN))
            
            new_nodes.append(TextNode(anchor_text, InlineTextType.LINK, url))
            
            remaining_text = sections[1] if len(sections) > 1 else ""
        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, InlineTextType.PLAIN))
    
    return new_nodes
    

def text_to_textnodes(text):

    
    nodes = [TextNode(text, InlineTextType.PLAIN)]
    
    nodes = split_nodes_delimiter(nodes, "**", InlineTextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", InlineTextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", InlineTextType.CODE)
    
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes

