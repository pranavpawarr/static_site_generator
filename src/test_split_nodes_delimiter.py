import unittest
from textnode import TextNode, InlineTextType
from split_nodes_delimiter import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    
    def test_code_block(self):
        """Test splitting with code block delimiter"""
        node = TextNode("This is text with a `code block` word", InlineTextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", InlineTextType.CODE)
        expected = [
            TextNode("This is text with a ", InlineTextType.PLAIN),
            TextNode("code block", InlineTextType.CODE),
            TextNode(" word", InlineTextType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_bold_delimiter(self):
        """Test splitting with bold delimiter"""
        node = TextNode("This is text with a **bolded phrase** in the middle", InlineTextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", InlineTextType.BOLD)
        expected = [
            TextNode("This is text with a ", InlineTextType.PLAIN),
            TextNode("bolded phrase", InlineTextType.BOLD),
            TextNode(" in the middle", InlineTextType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_italic_delimiter(self):
        """Test splitting with italic delimiter"""
        node = TextNode("This is *italic* text", InlineTextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "*", InlineTextType.ITALIC)
        expected = [
            TextNode("This is ", InlineTextType.PLAIN),
            TextNode("italic", InlineTextType.ITALIC),
            TextNode(" text", InlineTextType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_multiple_delimiters(self):
        """Test text with multiple delimited sections"""
        node = TextNode("Code `one` and code `two` here", InlineTextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", InlineTextType.CODE)
        expected = [
            TextNode("Code ", InlineTextType.PLAIN),
            TextNode("one", InlineTextType.CODE),
            TextNode(" and code ", InlineTextType.PLAIN),
            TextNode("two", InlineTextType.CODE),
            TextNode(" here", InlineTextType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_delimiter_at_start(self):
        """Test delimiter at the beginning of text"""
        node = TextNode("**bold** at start", InlineTextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", InlineTextType.BOLD)
        expected = [
            TextNode("bold", InlineTextType.BOLD),
            TextNode(" at start", InlineTextType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_delimiter_at_end(self):
        """Test delimiter at the end of text"""
        node = TextNode("At end **bold**", InlineTextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", InlineTextType.BOLD)
        expected = [
            TextNode("At end ", InlineTextType.PLAIN),
            TextNode("bold", InlineTextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_entire_text_delimited(self):
        """Test when entire text is delimited"""
        node = TextNode("**all bold**", InlineTextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", InlineTextType.BOLD)
        expected = [
            TextNode("all bold", InlineTextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_no_delimiter(self):
        """Test text with no delimiter"""
        node = TextNode("Plain text with no delimiter", InlineTextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", InlineTextType.CODE)
        expected = [
            TextNode("Plain text with no delimiter", InlineTextType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_non_text_node_unchanged(self):
        """Test that non-PLAIN nodes are not split"""
        node = TextNode("already bold", InlineTextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", InlineTextType.BOLD)
        expected = [
            TextNode("already bold", InlineTextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_multiple_nodes_mixed_types(self):
        """Test processing multiple nodes of mixed types"""
        nodes = [
            TextNode("Plain text with `code`", InlineTextType.PLAIN),
            TextNode("Already bold", InlineTextType.BOLD),
            TextNode("More `code` here", InlineTextType.PLAIN),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", InlineTextType.CODE)
        expected = [
            TextNode("Plain text with ", InlineTextType.PLAIN),
            TextNode("code", InlineTextType.CODE),
            TextNode("Already bold", InlineTextType.BOLD),
            TextNode("More ", InlineTextType.PLAIN),
            TextNode("code", InlineTextType.CODE),
            TextNode(" here", InlineTextType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_unclosed_delimiter_raises_exception(self):
        """Test that unclosed delimiter raises an exception"""
        node = TextNode("This has `unclosed code", InlineTextType.PLAIN)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", InlineTextType.CODE)
        self.assertIn("Invalid markdown syntax", str(context.exception))
        self.assertIn("unclosed delimiter", str(context.exception))
    
    def test_empty_delimited_section(self):
        """Test empty text between delimiters"""
        node = TextNode("Text with `` empty code", InlineTextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", InlineTextType.CODE)
        # Empty strings should be skipped
        expected = [
            TextNode("Text with ", InlineTextType.PLAIN),
            TextNode(" empty code", InlineTextType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_consecutive_delimiters(self):
        """Test multiple consecutive delimiter pairs"""
        node = TextNode("`one``two`", InlineTextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", InlineTextType.CODE)
        expected = [
            TextNode("one", InlineTextType.CODE),
            TextNode("two", InlineTextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)


if __name__ == "__main__":
    unittest.main()