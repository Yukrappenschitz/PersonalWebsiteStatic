
class HTMLNode: # "HTMLNode" class will represent a "node" in an HTML document tree (like a <p> tag and its contents, or an <a> tag and its contents). It can be block level or inline, and is designed to only output HTML.

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

        raise NotImplementedError('to_html method not implemented')



    def props_to_html(self) -> str|None: # 5. Add a props_to_html(self) method. It should return a formatted string representing the HTML attributes of the node. 

        if self.props is None: #  If self.props is None or empty, return an empty string
            return ''
                            # !!!! Notice the leading space character before href and before target. This is important. HTML attributes are always separated by spaces
        props_str = ''
        for prop in self.props:

            string = f' {prop}="{self.props[prop]}"'

            props_str += string

        return props_str

    def __repr__(self) -> str: # 6. Add a __repr__(self) method. Give yourself a way to print an HTMLNode object and see its tag, value, children, and props. This will be useful for your debugging.

        HTML_string_repr = f'HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})'

        return HTML_string_repr

    def __eq__(self, other: "HTMLNode") -> bool: # not necessary to implement for HTMLNode as it is not the same as TextNode

        if not isinstance(other, HTMLNode): # basic type checking on other to see if it is `HTMLNode` class object
            return False 

        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == self.children
            and self.props == other.props 
        )


class LeafNode(HTMLNode): # A LeafNode is a type of HTMLNode that represents a single HTML tag with no children. For example, a simple <p> tag with some text inside of i

    def __init__(self, 
                 tag: str | None,
                 value: str,
                 props: dict[str,str] | None = None
                 ) -> None:                  # 1. Create a child class of HTMLNode called LeafNode. Its constructor should differ slightly from the HTMLNode class because:

        super().__init__(tag, value, None, props)  # 1.c Use the super() function to call the constructor of the HTMLNode class. 
                                                 # !! remember the super method calls the parent class constructor and you can pass it the values to initialize the attributes of the child class DIRECTLY from the super().__init__(`arguments to pass`) call
                                                # !!! passing `None` as the children argument, 1.a The LeafNode class It should not allow for any children 
                                                # 1.b Both the value and tag data members should be required (even though the tag's value may be None), while props can remain optional like the HTMLNode constructor.

    
    def to_html(self) -> str:  # 2. Add a .to_html() method that renders a leaf node as an HTML string (by returning a string).

        if self.value == None: # 2.a If the leaf node has no value, it should raise a ValueError. All leaf nodes must have a value.
            raise ValueError('INVALID HTML: no value. LeafNode has no value. ALL LEAF NODES MUST HAVE A VALUE')

        if self.tag == None:  # 2.b If there is no tag (e.g. it's None), the value should be returned as raw text.
            return self.value 
        
        HTML_render_str = f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'  # parent HTMLNode already has a props to HTML method built that can be reused 

        return HTML_render_str

    
    def __repr__(self) -> str:

        LEAF_string_repr = f'LeafNode({self.tag}, {self.value}, {self.props})'

        return LEAF_string_repr

    def __eq__(self, other: "LeafNode") -> bool: # not necessary to implement for LeafNode as it is not the same as TextNode

        if not isinstance(other, LeafNode): # basic type checking on other to see if it is `LeafNode` class object
            return False 

        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == self.children 
            and self.props == other.props 
        )

class ParentNode(HTMLNode): # ParentNode class will handle the nesting of HTML nodes inside of one another. Any HTML node that's not "leaf" node (i.e. it has children) is a "parent" node.

    def __init__(
            self,
            tag: str,
            children: list[HTMLNode],
            props: dict[str,str] | None = None
                 ) -> None:          # 1. Create another child class of HTMLNode called ParentNode. Its constructor should differ from HTMLNode in that:
                             # 1.a The tag and children arguments are not optional
                             # 1.b It doesn't take a value argument, 
                             # 1.c props is optional
                            # 1.d (It's the exact opposite of the LeafNode class)
        
        super().__init__(tag, None, children, props)  # just using super to initailiaze parent class constructor by passing the values from ParentNode initialization

    def to_html(self) -> str:  # does not pretty print the HTML since most editors auto format HTML

        if self.tag == None:    # 2.1 If the object doesn't have a tag, raise a ValueError.
            raise ValueError('INVALID HTML. ParentNode tag has no tag.')
        
        if self.children == None:     # 2.2 If children is missing, raise a ValueError with a different message.
            raise ValueError('INVALID HTML. ParentNode children has no children. Parent Node MUST have children.')
                                   # 2.3 Otherwise, return a string representing the HTML tag of the node and its children. This should be a recursive method (each recursion being called on a nested child node).
        children_str = ''

        for children in self.children:  # !!! NEEDS this recursive approach. a ParentNode can contain another ParentNode, which can contain another ParentNode, and so on.
            children_str += children.to_html()
                                          # prints a single long asz line of html !!! DOES NOT PRETTY PRINT THE HTML Most editors are easily configured to auto-format HTML on save, so we won't worry about implementing that in our code.
        html_str = f'<{self.tag}>{children_str}</{self.tag}>'

        return html_str




# LEAF NODE explanation + text examples
"""
Time to render some HTML strings!

A LeafNode is a type of HTMLNode that represents a single HTML tag with no children. For example, a simple <p> tag with some text inside of it:

<p>This is a paragraph of text.</p>

We call it a "leaf" node because it's a "leaf" in the tree of HTML nodes. It's a node with no children. In this next example, <p> is not a leaf node, but <b> is.

<p>
  This is a paragraph. It can have a lot of text inside tbh.
  <b>This is bold text.</b>
  This is the last sentence.
</p>
"""

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
