from textnode import TextNode, InlineTextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Splits text nodes based on a delimiter and converts the delimited text to a specific type.
    
    Args:
        old_nodes: List of TextNode objects to process
        delimiter: String delimiter to split on (e.g., "**", "*", "`")
        text_type: InlineTextType to assign to delimited text
    
    Returns:
        List of TextNode objects with delimited sections split out
    
    Raises:
        ValueError: If delimiter is not properly closed
    """
    new_nodes = []
    
    for node in old_nodes:
        # If node is not plain text, keep it as-is
        if node.text_type != InlineTextType.PLAIN:
            new_nodes.append(node)
            continue
        
        # Split the text by the delimiter
        parts = node.text.split(delimiter)
        
        # Check if we have an even number of delimiters (must be closed)
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown syntax: unclosed delimiter '{delimiter}'")
        
        # Process the parts
        for i, part in enumerate(parts):
            # Skip empty strings
            if part == "":
                continue
            
            # Even indices are normal text, odd indices are delimited text
            if i % 2 == 0:
                new_nodes.append(TextNode(part, InlineTextType.PLAIN))
            else:
                new_nodes.append(TextNode(part, text_type))
    
    return new_nodes