
from enum import Enum 

class TextType(Enum):  # 4. In textnode.py create an enum called TextType. It should cover all the inline text types mentioned above.

    TEXT = "text" # text (plain)

    BOLD = "bold"  # **Bold text**

    ITALIC = "italic" # _Italic text_

    CODE = "code"  # `Code text`

    LINK = "link"  # Links, in this format: [anchor text](url)

    IMAGE = "image"  # Images, in this format: ![alt text](url)


class TextNode:  

    def __init__(self, text, text_type: TextType, url = None) -> None:  # 5. In textnode.py create a class called TextNode. It should have 3 properties that can be set in the constructor:
        
        self.text = text     # The text content of the node
        
        self.text_type: TextType = text_type   # The type of text this node contains, which is a member of the TextType enum
        
        self.url = url     # The URL of the link or image, if the text is a link. Default to None if nothing is passed in.

    def __eq__(self, other) -> bool: # 6. Create an __eq__ equality method on TextNode that compares self to another TextNode instance (other) and returns True if all of their properties are equal. Our future unit tests will rely on this method to compare objects.
          
          # just basic type checking using built in python function `isinstance()`
        if not isinstance(self, TextNode) or not isinstance(other, TextNode):
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

"""
Create a __repr__ method that returns a string representation of the TextNode object. It should look like this:

TextNode(TEXT, TEXT_TYPE, URL)

Where TEXT, TEXT_TYPE, and URL are the values of the text, text_type, and url properties, respectively.
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