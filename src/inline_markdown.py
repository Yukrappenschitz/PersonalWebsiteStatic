
from htmlnode import HTMLNode, LeafNode, ParentNode

from textnode import TextType, TextNode, text_node_to_html_node

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
                                                                    # It takes a list of "old nodes", a delimiter, and a text type. It should return a new list of nodes, where any "text" type nodes in the input list are (potentially) split into multiple nodes based on the syntax 
                                                                # it will take care of inline code, bold, and italic text using the same logic! The delimiter and matching text_type are the only thing that changes, e.g. ** for bold, _ for italic, and a backtick for code. 
                                                                # because it operates on an input list, we can call it multiple times to handle different types of delimiters. The order in which you check for different delimiters matters, which actually simplifies implementation.
    new_nodes = []

    for old_node in old_nodes: 
        
        if old_node.text_type != TextType.TEXT: # If an "old node" is not a TextType.TEXT type, just add it to the new list as-is, we only attempt to split "text" type objects (not bold, italic, etc).
            new_nodes.append(old_node)
            continue

        split_nodes = []
        sections = old_node.text.split(delimiter)  # passing in the given delimiter to split string along given delimiter

        if len(sections) % 2 == 0:    # built in python .split() function splits along given `"delimiter"` if given, and EVEN WORKS if the delimiter is at the end of the string, as it will still create a new index in the split list with an empty string so using `len % 2` works to check if delimiter is closed or not in markdown syntax
            raise ValueError(f'invalid markdown, formatted section not closed: {old_node.text}')  # If a matching closing delimiter is not found, just raise an exception with a helpful error message, that's invalid Markdown syntax.

        for i in range(len(sections)): # need to iterate over all given sections, we are given A RAW markdown String

            if sections[i] == "":
                continue 
            
            if i % 2 == 0:  # remember in python `0 % 2` = 0 
                split_nodes.append( TextNode(sections[i], TextType.TEXT) )  # if `i` is even/0, means we have hit a section that is Text Type `TEXT`, just normal text, and we are not formatting this section in this function 
            
            else:              # if `i`` is ODD, means we have hit a delimiter section and need to switch the Text Type to given `text_type`
                split_nodes.append( TextNode(sections[i], text_type) )       

        new_nodes.extend(split_nodes)   # !!! important to use extend so EACH NODE GETS ADDED one by one instead of as a single item
    
    return new_nodes



# split_nodes_delimiter Function Thought Process and Functionality

"""
a new function 

`def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:`

It takes a list of "old nodes", a delimiter, and a text type. It should return a new list of nodes, where any "text" type nodes in the input list are (potentially) split into multiple nodes based on the syntax. For example, given the following input:

node = TextNode("This is text with a `code block` word", TextType.TEXT)
new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

new_nodes becomes:

[
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT),
]

The beauty of this function is that it will take care of inline code, bold, and italic text using the same logic! 
The delimiter and matching text_type are the only thing that changes, e.g. ** for bold, _ for italic, and a backtick for code. Also, because it operates on an input list, we can call it multiple times to handle different types of delimiters. 
The order in which you check for different delimiters matters, which actually simplifies implementation.

Some pointers:

If an "old node" is not a TextType.TEXT type, just add it to the new list as-is, we only attempt to split "text" type objects (not bold, italic, etc).

If a matching closing delimiter is not found, just raise an exception with a helpful error message, that's invalid Markdown syntax.

The .split() string method was useful

The .extend() list method was useful

Write a bunch of tests. Be sure to test various types of delimiters.
"""

