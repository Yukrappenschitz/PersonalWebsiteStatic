
import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
# own shiety useless crafted tests
    def test_eq_own(self):
        node = HTMLNode("p", "test paragraph",None,{"href": "https://www.google.com"})
        node2 = HTMLNode("p", "test paragraph",None,{"href": "https://www.google.com"})

        self.assertEqual(node, node2)

    def test_eq_false_own(self):
        node = HTMLNode("p", "test paragraph",None,{"href": "https://www.google.com"})
        node2 = HTMLNode("a", "diff_test paragraph",None,None)
        
        self.assertNotEqual(node, node2)

    def test_repr_own(self):

        node = HTMLNode("p", "test paragraph",None,{"href": "https://www.google.com"})
        
        self.assertNotEqual(node, repr(node))

# some given, some tweaked tests to test if all the given fields in the HTMLNode constructor are working properly according to their types 

    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

class TestLeafNode(unittest.TestCase):
    
# some given, some tweaked
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")



if __name__ == "__main__":
    unittest.main()