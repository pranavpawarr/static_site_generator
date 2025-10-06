import unittest
from split_nodes_delimiter import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
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


class TestSplitNodesImage(unittest.TestCase):
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            InlineTextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", InlineTextType.PLAIN),
                TextNode("image", InlineTextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", InlineTextType.PLAIN),
                TextNode("second image", InlineTextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    
    def test_split_image_single(self):
        node = TextNode(
            "This is text with an ![image](https://example.com/img.png)",
            InlineTextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", InlineTextType.PLAIN),
            TextNode("image", InlineTextType.IMAGE, "https://example.com/img.png"),
        ]
        self.assertListEqual(expected, new_nodes)
    
    def test_split_image_no_images(self):
        node = TextNode("This is plain text with no images", InlineTextType.PLAIN)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is plain text with no images", InlineTextType.PLAIN),
        ]
        self.assertListEqual(expected, new_nodes)


class TestSplitNodesLink(unittest.TestCase):
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            InlineTextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", InlineTextType.PLAIN),
            TextNode("to boot dev", InlineTextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", InlineTextType.PLAIN),
            TextNode("to youtube", InlineTextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(expected, new_nodes)
    
    def test_split_link_single(self):
        node = TextNode(
            "Click [here](https://example.com) for more",
            InlineTextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Click ", InlineTextType.PLAIN),
            TextNode("here", InlineTextType.LINK, "https://example.com"),
            TextNode(" for more", InlineTextType.PLAIN),
        ]
        self.assertListEqual(expected, new_nodes)
    
    def test_split_link_no_links(self):
        node = TextNode("This is plain text with no links", InlineTextType.PLAIN)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is plain text with no links", InlineTextType.PLAIN),
        ]
        self.assertListEqual(expected, new_nodes)


class TestTextToTextNodes(unittest.TestCase):
    
    def test_text_to_textnodes_all_types(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", InlineTextType.PLAIN),
            TextNode("text", InlineTextType.BOLD),
            TextNode(" with an ", InlineTextType.PLAIN),
            TextNode("italic", InlineTextType.ITALIC),
            TextNode(" word and a ", InlineTextType.PLAIN),
            TextNode("code block", InlineTextType.CODE),
            TextNode(" and an ", InlineTextType.PLAIN),
            TextNode("obi wan image", InlineTextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", InlineTextType.PLAIN),
            TextNode("link", InlineTextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(nodes, expected)
    
    def test_text_to_textnodes_plain_only(self):
        text = "This is just plain text with no formatting"
        nodes = text_to_textnodes(text)
        expected = [TextNode("This is just plain text with no formatting", InlineTextType.PLAIN)]
        self.assertListEqual(nodes, expected)
    
    def test_text_to_textnodes_bold_only(self):
        text = "This has **bold text** in it"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This has ", InlineTextType.PLAIN),
            TextNode("bold text", InlineTextType.BOLD),
            TextNode(" in it", InlineTextType.PLAIN),
        ]
        self.assertListEqual(nodes, expected)
    
    def test_text_to_textnodes_mixed_formatting(self):
        text = "**bold** and _italic_ together"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold", InlineTextType.BOLD),
            TextNode(" and ", InlineTextType.PLAIN),
            TextNode("italic", InlineTextType.ITALIC),
            TextNode(" together", InlineTextType.PLAIN),
        ]
        self.assertListEqual(nodes, expected)
    
    def test_text_to_textnodes_multiple_images(self):
        text = "![img1](url1.png) and ![img2](url2.png)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("img1", InlineTextType.IMAGE, "url1.png"),
            TextNode(" and ", InlineTextType.PLAIN),
            TextNode("img2", InlineTextType.IMAGE, "url2.png"),
        ]
        self.assertListEqual(nodes, expected)


if __name__ == "__main__":
    unittest.main()
