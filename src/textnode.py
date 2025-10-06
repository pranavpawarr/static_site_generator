from htmlnode import LeafNode
from enum import Enum

class InlineTextType(Enum):
    PLAIN = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    def __init__(self, text, text_type , url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return NotImplemented
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url)
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    t = text_node.text_type.value if isinstance(text_node.text_type, InlineTextType) else text_node.text_type

    if t == "text":
        return LeafNode(None, text_node.text)
    if t == "bold":
        return LeafNode("b", text_node.text)
    if t == "italic":
        return LeafNode("i", text_node.text)
    if t == "code":
        return LeafNode("code", text_node.text)
    if t == "link":
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if t == "image":
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Invalid text type: {t}")