import unittest
from split_nodes_delimiter import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
)

from textnode import TextNode, InlineTextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", InlineTextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", InlineTextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", InlineTextType.PLAIN),
                TextNode("bolded", InlineTextType.BOLD),
                TextNode(" word", InlineTextType.PLAIN),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", InlineTextType.PLAIN
        )
        new_nodes = split_nodes_delimiter([node], "**", InlineTextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", InlineTextType.PLAIN),
                TextNode("bolded", InlineTextType.BOLD),
                TextNode(" word and ", InlineTextType.PLAIN),
                TextNode("another", InlineTextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", InlineTextType.PLAIN
        )
        new_nodes = split_nodes_delimiter([node], "**", InlineTextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", InlineTextType.PLAIN),
                TextNode("bolded word", InlineTextType.BOLD),
                TextNode(" and ", InlineTextType.PLAIN),
                TextNode("another", InlineTextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", InlineTextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", InlineTextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", InlineTextType.PLAIN),
                TextNode("italic", InlineTextType.ITALIC),
                TextNode(" word", InlineTextType.PLAIN),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", InlineTextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", InlineTextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", InlineTextType.ITALIC)
        self.assertEqual(
            [
                TextNode("bold", InlineTextType.BOLD),
                TextNode(" and ", InlineTextType.PLAIN),
                TextNode("italic", InlineTextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", InlineTextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", InlineTextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", InlineTextType.PLAIN),
                TextNode("code block", InlineTextType.CODE),
                TextNode(" word", InlineTextType.PLAIN),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )


if __name__ == "__main__":
    unittest.main()