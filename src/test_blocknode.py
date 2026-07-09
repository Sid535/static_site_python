import unittest
from blocknode import markdown_to_blocks, markdown_to_html_node


class TestBlockMarkdown(unittest.TestCase):
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
        
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
        
    def test_single_paragraph(self):
        md = "This is just one paragraph of text."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is just one paragraph of text.</p></div>",
        )

    def test_heading_and_paragraph(self):
        md = """
# Main Title

This is a paragraph under the title.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Main Title</h1><p>This is a paragraph under the title.</p></div>",
        )
    
    def test_all_block_types_together(self):
        md = """
# Heading

This is a paragraph with **bold** and _italic_ text.
with newlines

```
code block line one
code block line two
```

> A quoted line
> and another

- unordered item one
- unordered item two

1. ordered item one
2. ordered item two
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading</h1><p>This is a paragraph with <b>bold</b> and <i>italic</i> text. with newlines</p><pre><code>code block line one\ncode block line two\n</code></pre><blockquote>A quoted line and another</blockquote><ul><li>unordered item one</li><li>unordered item two</li></ul><ol><li>ordered item one</li><li>ordered item two</li></ol></div>",
        )
    
    def test_list_with_links_and_images(self):
        md = """
- Check out [this link](https://example.com)
- And this image ![alt text](https://example.com/img.png)
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ul><li>Check out <a href="https://example.com">this link</a></li>'
            '<li>And this image <img src="https://example.com/img.png" alt="alt text"></img></li></ul></div>',
        )
    
    def test_code_block_ignores_inline_markdown(self):
        md = """
```
this **should not** be _parsed_
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>this **should not** be _parsed_\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
    

if __name__ == "__main__":
    unittest.main()