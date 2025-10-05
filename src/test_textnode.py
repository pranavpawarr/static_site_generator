import unittest
from textnode import TextNode, InlineTextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):

    def test_eq(self):
        node = TextNode("This is a text node", InlineTextType.BOLD)
        node2 = TextNode("This is a text node", InlineTextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        node = TextNode("This is a text node", InlineTextType.BOLD)
        node2 = TextNode("Different text", InlineTextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_type(self):
        node = TextNode("This is a text node", InlineTextType.BOLD)
        node2 = TextNode("This is a text node", InlineTextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_same_object(self):
        node = TextNode("Sample", InlineTextType.BOLD)
        self.assertEqual(node, node)

    def test_not_eq_with_url_none(self):
        node1 = TextNode("Sample", InlineTextType.BOLD, url=None)
        node2 = TextNode("Sample", InlineTextType.BOLD, url="http://example.com")
        self.assertNotEqual(node1, node2)

    def test_eq_both_url_none(self):
        node1 = TextNode("Sample", InlineTextType.BOLD, url=None)
        node2 = TextNode("Sample", InlineTextType.BOLD, url=None)
        self.assertEqual(node1, node2)

    def test_not_eq_different_text_type(self):
        node1 = TextNode("Sample", InlineTextType.BOLD)
        node2 = TextNode("Sample", InlineTextType.ITALIC)
        self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()
