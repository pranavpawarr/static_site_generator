import unittest
from markdown_to_blocks import markdown_to_blocks , block_to_block_type , BlockType


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


if __name__ == "__main__":
    unittest.main()