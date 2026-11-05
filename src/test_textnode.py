import unittest  # part of python standard library

# specific imports
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):

# own shiety crafted tests
    def test_not_eq(self):

        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a Italic node", TextType.ITALIC)

        self.assertNotEqual(node, node2)

    def test_url_not_eq(self): 

        node = TextNode("This is a link node", TextType.LINK, "test_url")
        node2 = TextNode("This is a different link node", TextType.LINK, "diff_test_url")

        self.assertNotEqual(node, node2)

# some given tests, some tweaked
    def test_eq(self):
        
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)

        self.assertEqual(node, node2)  # 2. This test creates two TextNode objects with the same properties and asserts that they are equal. Notice the missing url argument which should have a default value of None. If you run your tests with ./test.sh, you should see that the test passes.

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )

# UNIT TESTS FOR FUNCTION `text_node_to_html_node` 
class TestTextNodeToHTMLNodeFunction(unittest.TestCase):

# some given, some tweaked 
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node") 

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

    def test_invalid_text_type(self):
            node = TextNode("This is an invalid Text Type", TextType.INVALID)
            html_node = text_node_to_html_node(node)
            self.assertNotEqual(html_node.tag, "b")
            self.assertNotEqual(html_node.value, "This is bold")


if __name__ == "__main__":
    unittest.main() 


# FIRST TEST CASES FOR `TextNode` class

"""
2. This test creates two TextNode objects with the same properties and asserts that they are equal. Notice the missing url argument which should have a default value of None. If you run your tests with ./test.sh, you should see that the test passes.

3. Add some test cases by adding methods to the TestTextNode class to verify that the TextNode class works as expected. You can use the following methods to compare the objects:

self.assertEqual - if the inputs are equal the test passes

self.assertNotEqual - if the inputs are not equal the test passes

4. Add even more test cases (at least 3 in total) to check various edge cases, like when the url property is None, or when the text_type property is different. You'll want to make sure that when properties are different, the TextNode objects are not equal.
"""