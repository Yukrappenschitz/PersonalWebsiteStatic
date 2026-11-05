
from enum import Enum 
from htmlnode import HTMLNode, LeafNode, ParentNode

class TextType(Enum):  # 4. In textnode.py create an enum called TextType. It should cover all the inline text types mentioned above.

    TEXT = "text" # text (plain)

    BOLD = "bold"  # **Bold text**

    ITALIC = "italic" # _Italic text_

    CODE = "code"  # `Code text`

    LINK = "link"  # Links, in this format: [anchor text](url)

    IMAGE = "image"  # Images, in this format: ![alt text](url)


class TextNode:  

    def __init__(
            self, 
            text: str, 
            text_type: TextType, 
            url: str| None = None
            ) -> None:  # 5. In textnode.py create a class called TextNode. It should have 3 properties that can be set in the constructor:
        
        self.text = text     # The text content of the node
        
        self.text_type: TextType = text_type   # The type of text this node contains, which is a member of the TextType enum
        
        self.url = url     # The URL of the link or image, if the text is a link. Default to None if nothing is passed in.

    def __eq__(self, other: "TextNode") -> bool: # 6. Create an __eq__ equality method on TextNode that compares self to another TextNode instance (other) and returns True if all of their properties are equal. Our future unit tests will rely on this method to compare objects.
          
          # just basic type checking using built in python function `isinstance()`
        if not isinstance(other, TextNode):
            return False 

        # Python doesn't automatically compare all your class attributes when you implement __eq__. You need to explicitly tell it which properties to compare. 
        # this should just evaluate to a bool 
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        ) 

    def __repr__(self) -> str:  # 7. a __repr__ method that returns a string representation of the TextNode object. 

        string = f'TextNode({self.text}, {self.text_type.value}, {self.url})'  # can get the string representation of the text_type enum by using the .value field.

        return string 


def text_node_to_html_node(text_node: TextNode) -> LeafNode: # It should handle each type of the TextType enum. If it gets a TextNode that is none of those types, it should raise an exception. Otherwise, it should return a new LeafNode object.

    match text_node.text_type:

        case TextType.TEXT:   # TextType.TEXT: This should return a LeafNode with no tag, just a raw text value.
            return LeafNode(None, text_node.text, None) 

        case TextType.BOLD:    # TextType.BOLD: This should return a LeafNode with a "b" tag and the text
            return LeafNode("b", text_node.text, None)

        case TextType.ITALIC:   # TextType.ITALIC: "i" tag, text
            return LeafNode("i", text_node.text, None) 

        case TextType.CODE:      # TextType.CODE: "code" tag, text
            return LeafNode("code", text_node.text, None)

        case TextType.LINK:    # TextType.LINK: "a" tag, anchor text, and "href" prop
            if text_node.url is None:
                raise ValueError("INVALID URL")
            return LeafNode("a", text_node.text, {"href": text_node.url})

        case TextType.IMAGE:    # TextType.IMAGE: "img" tag, empty string value, "src" and "alt" props ("src" is the image URL, "alt" is the alt text) 
            if text_node.url is None:
                raise ValueError("INVALID URL")
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text} )

        case _:
            raise ValueError(f'INVALID TEXT TYPE: {text_node.text_type}. Does not match any implemented Text Types in TextType enum.')


"""
Create a __repr__ method that returns a string representation of the TextNode object. It should look like this:

TextNode(TEXT, TEXT_TYPE, URL)

Where TEXT, TEXT_TYPE, and URL are the values of the text, text_type, and url properties, respectively.
""" 

# TEXT NODE AND HTML NODE THOUGHT PROCESS

"""
Our "TextNode" class represents the various types of inline text that can exist in HTML and Markdown.

Our "HTMLNode" class will represent a "node" in an HTML document tree (like a <p> tag and its contents, or an <a> tag and its contents). It can be block level or inline, and is designed to only output HTML.
"""


# ENUM AND CLASS CREATION THOUGHT PROCESS 

""" We're going to need a way to represent all the different types of inline text. We're going to be parsing Markdown text, and outputting it to HTML, so we need an intermediate representation of the text in our code.

When I say "inline" I just mean text that is part of a larger block of text. For us, this includes:

text (plain)

**Bold text**

_Italic text_

`Code text`

Links, in this format: [anchor text](url)

Images, in this format: ![alt text](url)

Everything else we're considering block level, like headings, paragraphs, and bullet lists, and we'll handle those later.
"""