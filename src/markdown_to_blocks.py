from enum import Enum

from htmlnode import ParentNode
from split_nodes_delimiter import text_to_textnodes
from textnode import TextNode, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6


def block_to_block_type(block):
    if not block:
        return BlockType.PARAGRAPH
   
    lines = block.split("\n")
    
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    is_ordered = True
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED_LIST  
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.PARAGRAPH:
            # Create a <p> tag with inline markdown parsed
            child_nodes = text_to_children(block)
            paragraph_node = ParentNode("p", child_nodes)
            children.append(paragraph_node)
        
        elif block_type == BlockType.HEADING:
            # Determine heading level (count # characters)
            level = 0
            for char in block:
                if char == "#":
                    level += 1
                else:
                    break
            # Remove the # characters and space
            text = block[level + 1:]
            child_nodes = text_to_children(text)
            heading_node = ParentNode(f"h{level}", child_nodes)
            children.append(heading_node)
        
        elif block_type == BlockType.CODE:
            # Remove the ``` delimiters
            code_text = block[3:-3]
            # Don't parse inline markdown for code blocks
            code_node = TextNode(code_text, "text")
            code_html = text_node_to_html_node(code_node)
            # Wrap in <pre><code>
            code_parent = ParentNode("code", [code_html])
            pre_node = ParentNode("pre", [code_parent])
            children.append(pre_node)
        
        elif block_type == BlockType.QUOTE:
            # Remove > from each line and join
            lines = block.split("\n")
            quote_lines = []
            for line in lines:
                # Remove the > and optional space
                if line.startswith("> "):
                    quote_lines.append(line[2:])
                elif line.startswith(">"):
                    quote_lines.append(line[1:])
            quote_text = "\n".join(quote_lines)
            child_nodes = text_to_children(quote_text)
            quote_node = ParentNode("blockquote", child_nodes)
            children.append(quote_node)
        
        elif block_type == BlockType.UNORDERED_LIST:
            # Create <ul> with <li> children
            lines = block.split("\n")
            list_items = []
            for line in lines:
                # Remove "- " from the start
                item_text = line[2:]
                item_children = text_to_children(item_text)
                li_node = ParentNode("li", item_children)
                list_items.append(li_node)
            ul_node = ParentNode("ul", list_items)
            children.append(ul_node)
        
        elif block_type == BlockType.ORDERED_LIST:
            # Create <ol> with <li> children
            lines = block.split("\n")
            list_items = []
            for line in lines:
                # Remove "N. " from the start (where N is the number)
                # Find the first ". " and remove everything before and including it
                dot_index = line.index(". ")
                item_text = line[dot_index + 2:]
                item_children = text_to_children(item_text)
                li_node = ParentNode("li", item_children)
                list_items.append(li_node)
            ol_node = ParentNode("ol", list_items)
            children.append(ol_node)
    
    # Wrap all blocks in a parent div
    return ParentNode("div", children)
