import unittest
from markdown_to_blocks import extract_title, markdown_to_blocks , block_to_block_type , BlockType


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    
    def test_block_type_heading_h1(self):
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_block_type_heading_h2(self):
        block = "## Heading 2"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_block_type_heading_h3(self):
        block = "### Heading 3"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_block_type_heading_h4(self):
        block = "#### Heading 4"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_block_type_heading_h5(self):
        block = "##### Heading 5"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_block_type_heading_h6(self):
        block = "###### Heading 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_block_type_heading_no_space(self):
        block = "#NoSpace"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_block_type_heading_too_many_hashes(self):
        block = "####### Seven hashes"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_block_type_code(self):
        block = "```\ncode block\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_block_type_code_single_line(self):
        block = "```code```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_block_type_code_with_language(self):
        block = "```python\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_block_type_quote_single_line(self):
        block = ">This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_block_type_quote_multi_line(self):
        block = ">Line 1\n>Line 2\n>Line 3"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_block_type_quote_with_space(self):
        block = "> Quote with space"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_block_type_quote_incomplete(self):
        block = ">Line 1\nNot a quote\n>Line 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_block_type_unordered_list_single(self):
        block = "- Item 1"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_block_type_unordered_list_multi(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_block_type_unordered_list_no_space(self):
        block = "-Item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_block_type_unordered_list_incomplete(self):
        block = "- Item 1\nNot an item\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_block_type_ordered_list_single(self):
        block = "1. First item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_block_type_ordered_list_multi(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_block_type_ordered_list_wrong_order(self):
        block = "1. First\n3. Third\n2. Second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_block_type_ordered_list_not_starting_at_1(self):
        block = "2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_block_type_ordered_list_no_space(self):
        block = "1.Item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_block_type_ordered_list_no_period(self):
        block = "1 Item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_block_type_ordered_list_large_numbers(self):
        block = "1. First\n2. Second\n3. Third\n4. Fourth\n5. Fifth\n6. Sixth\n7. Seventh\n8. Eighth\n9. Ninth\n10. Tenth"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_block_type_paragraph_simple(self):
        block = "This is a simple paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_block_type_paragraph_multiline(self):
        block = "This is line 1\nThis is line 2\nThis is line 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_block_type_paragraph_with_formatting(self):
        block = "This has **bold** and _italic_ and `code`"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_block_type_paragraph_empty(self):
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestExtractTitle(unittest.TestCase):
    
    def test_simple_h1(self):
        """Test extracting a simple h1 header"""
        result = extract_title("# Hello")
        self.assertEqual(result, "Hello")
    
    def test_h1_with_leading_whitespace(self):
        """Test h1 with leading whitespace in the line"""
        result = extract_title("   # Welcome")
        self.assertEqual(result, "Welcome")
    
    def test_h1_with_trailing_whitespace(self):
        """Test h1 with trailing whitespace after the text"""
        result = extract_title("# My Title   ")
        self.assertEqual(result, "My Title")
    
    def test_h1_with_both_leading_and_trailing_whitespace(self):
        """Test h1 with whitespace on both sides"""
        result = extract_title("   # My Title   ")
        self.assertEqual(result, "My Title")
    
    def test_h1_with_multiple_words(self):
        """Test h1 with multiple words"""
        result = extract_title("# This is a Long Title")
        self.assertEqual(result, "This is a Long Title")
    
    def test_h1_in_multiline_markdown(self):
        """Test extracting h1 from markdown with multiple lines"""
        markdown = """Some text
# Main Title
## Subtitle
More content"""
        result = extract_title(markdown)
        self.assertEqual(result, "Main Title")
    
    def test_h1_not_first_line(self):
        """Test h1 that's not on the first line"""
        markdown = """Paragraph text

# Title Here

More text"""
        result = extract_title(markdown)
        self.assertEqual(result, "Title Here")
    
    def test_no_h1_raises_exception(self):
        """Test that missing h1 raises an exception"""
        with self.assertRaises(Exception) as context:
            extract_title("## Only h2 headers here")
        self.assertEqual(str(context.exception), "No h1 header found in markdown")
    
    def test_only_h2_raises_exception(self):
        """Test that only h2 headers raises an exception"""
        markdown = """## Header 2
### Header 3
#### Header 4"""
        with self.assertRaises(Exception):
            extract_title(markdown)
    
    def test_empty_markdown_raises_exception(self):
        """Test that empty markdown raises an exception"""
        with self.assertRaises(Exception):
            extract_title("")
    
    def test_no_headers_raises_exception(self):
        """Test that markdown without any headers raises an exception"""
        with self.assertRaises(Exception):
            extract_title("Just some plain text without any headers")
    
    def test_h1_with_extra_spaces_after_hash(self):
        """Test h1 with multiple spaces after the #"""
        result = extract_title("#    Title with Spaces")
        self.assertEqual(result, "Title with Spaces")
    
    def test_first_h1_is_returned(self):
        """Test that the first h1 is returned when multiple exist"""
        markdown = """# First Title
Some content
# Second Title"""
        result = extract_title(markdown)
        self.assertEqual(result, "First Title")

if __name__ == "__main__":
    unittest.main()