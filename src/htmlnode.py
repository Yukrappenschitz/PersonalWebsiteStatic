


class HTMLNode:

    def __init__(
            self, 
            tag: str | None = None, 
            value: str | None = None, 
            children: list["HTMLNode"] | None = None,
            props: dict[str, str] | None = None
            ) -> None:                    # 2. HTMLNode class should have 4 data members set in the constructor:
                                      # 3. Perhaps counterintuitively, every data member should be optional and default to None
        self.tag = tag   # tag - A string representing the HTML tag name (e.g. "p", "a", "h1", etc.) | An HTMLNode without a tag will just render as raw text
        
        self.value = value # value - A string representing the value of the HTML tag (e.g. the text inside a paragraph) | An HTMLNode without a value will be assumed to have children
        
        self.children = children # children - A list of HTMLNode objects representing the children of this node | An HTMLNode without children will be assumed to have a value
        
        self.props = props  # props - A dictionary of key-value pairs representing the attributes of the HTML tag (properties). For example, a link (<a> tag) might have {"href": "https://www.google.com"} | An HTMLNode without props simply won't have any attributes

    def to_html(self): # 4. Add a to_html(self) method. For now, it should just raise a NotImplementedError. Child classes will override this method to render themselves as HTML.

        raise NotImplementedError("to_html method not implemented")



    def props_to_html(self) -> str|None: # 5. Add a props_to_html(self) method. It should return a formatted string representing the HTML attributes of the node. 

        if self.props is None: #  If self.props is None or empty, return an empty string
            return ''
                            # !!!! Notice the leading space character before href and before target. This is important. HTML attributes are always separated by spaces
        props_str = ''
        for prop in self.props:

            string = f' {prop}="{self.props[prop]}"'

            props_str += string

        return props_str

    def __repr__(self): # 6. Add a __repr__(self) method. Give yourself a way to print an HTMLNode object and see its tag, value, children, and props. This will be useful for your debugging.

        string_representation = f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

        return string_representation

    def __eq__(self, other: "HTMLNode") -> bool: # not necessary to implement for HTMLNode as it is not the same as TextNode

        if not isinstance(other, HTMLNode): # basic type checking on other to see if it is `HTMLNode` class object
            return False 

        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == self.children
            and self.props == other.props 
        )


# method props_to_html example output
"""
 For example, if self.props is:

{
    "href": "https://www.google.com",
    "target": "_blank",
}

Then self.props_to_html() should return:

 href="https://www.google.com" target="_blank"

Notice the leading space character before href and before target. This is important. !!!!! HTML attributes are always separated by spaces. If self.props is None or empty, return an empty string.
"""


# HTML NODE AND TEXT NODE CLASSES THOUGHT PROCESS

"""
Our "TextNode" class represents the various types of inline text that can exist in HTML and Markdown.

Our "HTMLNode" class will represent a "node" in an HTML document tree (like a <p> tag and its contents, or an <a> tag and its contents). It can be block level or inline, and is designed to only output HTML.
"""
