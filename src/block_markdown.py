from enum import Enum
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode

from inline_markdown import split_nodes_delimiter, split_nodes_link, split_nodes_image, text_to_textnodes

class BlockType(Enum):  # Our static site generator supports 6 types of markdown blocks
                             # 1. Create a BlockType enum with the block types 
    
    HEADING = "heading"  # Headings start with 1-6 # characters, followed by a space and then the heading text

    CODE = "code"     # Multiline Code blocks must start with 3 backticks and a newline, then end with 3 backticks.
    
    QUOTE = "quote"   # Every line in a quote block must start with a "greater-than" character: > followed by the quote text. A space after > is allowed but not required

    ULIST = "unordered_list"  # Every line in an unordered list block must start with a - character, followed by a space.

    OLIST = "ordered_list"  # Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.

    PARAGRAPH = "paragraph" # If none of the above conditions are met, the block is a normal paragraph. 


def block_to_block_type(block: str) -> BlockType:  # function that takes a single block of markdown text as input and returns the BlockType representing the type of block it is
                                                    # can assume all leading and trailing whitespace were already stripped 
    
    lines = block.split("\n")  # !!! Splitting the block into lines for parsing

    # HEADINGs start with 1-6 # characters, followed by a space and then the heading text.
    
    if block.startswith( ("# ", "## ", "### ", "#### ", "##### ", "###### ") ):
        return BlockType.HEADING 

    # CODE   Multiline Code blocks must start with 3 backticks and a newline, then end with 3 backticks.
    
    if len(lines) > 1 and ( lines[0].startswith("```") ) and ( lines[-1].endswith("```") ):
        return BlockType.CODE 

    # QUOTE Every line in a quote block must start with a "greater-than" character: > followed by the quote text. A space after > is allowed but not required.
    
    if block.startswith(">"):
        for line in lines:

            if not line.startswith(">"):
                return BlockType.PARAGRAPH  # If none of the above conditions are met, the block is a normal paragraph.
            
        return BlockType.QUOTE 

    # UNORDERED LIST Every line in an unordered list block must start with a - character, followed by a space.

    if block.startswith("- "):
        for line in lines:

            if not line.startswith("- "):
                return BlockType.PARAGRAPH

        return BlockType.ULIST 

    # ORDERED LIST Every line in an ordered list block must start with a number followed by a . character and a space.  

    if block.startswith("1. "):  # The number must start at 1
        i = 1
        for line in lines:

            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH

            i+= 1  # and increment by 1 for each line.

        return BlockType.OLIST 

    # PARAGRAPH  # redundant # If none of the above conditions are met, the block is a normal paragraph.

    return BlockType.PARAGRAPH
    

def markdown_to_blocks(markdown: str) -> list[str] :   # It takes a raw Markdown string (representing a full document) as input and returns a list of "block" strings. 

    split_blocks = markdown.split("\n\n")  #  used to split a string into blocks based on a delimiter (\n\n is a double newline).

    filtered_blocks = []

    for block in split_blocks:    # need to iterate over all blocks to clean and sanitize whitespaces and empty blocks
        
        block = block.strip()  # should .strip() any leading or trailing whitespace from each block.

        if block != '':        # Remove any "empty" blocks due to excessive newlines.
            filtered_blocks.append(block)
            
    return filtered_blocks 


# CONVERTING MARKDOWN raw text TO HTMLNodes

def markdown_to_html_node(markdown: str): #  converts a full markdown document into a single parent HTMLNode. 
                                     # That one parent HTMLNode should (obviously) contain many child HTMLNode objects representing the nested elements.
    
    children = []

    blocks = markdown_to_blocks(markdown) # 1. Split the markdown into blocks (you already have a function for this)

    for block in blocks:  # 2. Loop over each block:
        html_node = block_to_html_node(block)
        children.append(html_node)

    return ParentNode("div",children, None)    # Make all the block nodes children under a single parent HTML node (which should just be a div) and return it.


def text_to_children(text: str) -> list[HTMLNode]: # function that works for all block types. It takes a string of text and returns a list of HTMLNodes that represent the inline markdown using previously created functions (like TextNode -> HTMLNode)

    html_nodes = []   # will be children HTMLNodes
    text_nodes = text_to_textnodes(text)  # taking the `block` raw markdown text and parsing and converting it into TextNodes

    for text_node in text_nodes:    # iterating over the TextNodes

        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)    # taking the invidual TextNode and converting to individual HTMLNodes

    return html_nodes   # all the individual HTMLNodes represents all the children of the given `block` from caller function


def block_to_html_node(block:str): # Caller function to call HELPER functions based on BlockType
                                                        # GIVEN an individual block type that then needs to be parsed by helper functions into children HTMLNodes
        type_block = block_to_block_type(block)   # 2.1 Determine the type of block (you already have a function for this) 

        match type_block:              # 2.2  Based on the type of block, create a new HTMLNode with the proper data

            case BlockType.PARAGRAPH:
                return paragraph_to_html_node(block)
            
            case BlockType.HEADING:
                return heading_to_html_node(block)

            case BlockType.CODE:
                return code_to_html_node(block)
            
            case BlockType.OLIST:
                return olist_to_html_node(block)

            case BlockType.ULIST:
                return ulist_to_html_node(block)

            case BlockType.QUOTE:
                return quote_to_html_node(block)

            case _:
                raise ValueError(f'invalid block type or block type not supported: {block}')


def heading_to_html_node(block: str) -> ParentNode:  # Headings should be surrounded by a <h1> to <h6> tag, depending on the number of # characters.

    level = 0

    for char in block:

        if char == "#":
            level += 1
        else:         
            break             # need to break if we hit a whitespace, means we have hit the number of "#" in the heading

        if level + 1 >= len(block):
            raise ValueError(f'invalid heading level: {level} in {block}')

    text = block[ level + 1: ]  # need to remover "#" characters and whitespace, level + 1 to account for whitespace 

    children = text_to_children(text)  # calling helper function that turns this `text_filtered` into text nodes and then turns those text nodes into html nodes and returns those html nodes as a list of HTMLNodes 

    return ParentNode(f'h{level}', children)


def paragraph_to_html_node(block: str) -> ParentNode:  # Paragraphs should be surrounded by a <p> tag. I removed the newlines and replaced them with spaces.

    lines = block.split("\n")      # since its a paragraph need to strip "\n" characters to turn the multi-line entire paragraph into a single line in HTML format <p> "paragraph text" </p>
    
    single_line = " ".join(lines)     # need to join back together the list of stripped strings into a single line
    
    children = text_to_children(single_line)   # calling helper function that turns this `text_filtered` into text nodes and then turns those text nodes into html nodes and returns those html nodes as a list of HTMLNodes 

    return ParentNode("p", children)


def olist_to_html_node(block: str) -> ParentNode:  # Ordered list blocks should be surrounded by a <ol> tag, and each list item should be surrounded by a <li> tag.

    list_items = block.split("\n")   # gives a list of the items in the ordered list

    html_items = []

    for item in list_items:

        parts = item.split(". ", 1) # separating the numbered ordered list into two parts, ("{1.}", "text in ordered list")
        
        text = parts[1]  # accessing only the text part of the item 

        children = text_to_children(text) # calling helper function that turns this `text_filtered` into text nodes and then turns those text nodes into html nodes and returns those html nodes as a list of HTMLNodes 
                   
        html_items.append( ParentNode("li", children) ) # Creating a Node for each item in the list # each list item should be surrounded by a <li> tag

    return ParentNode("ol", html_items)   # # Ordered list blocks should be surrounded by a <ol> tag # adding the items that are now all converedted into HTML Parent Nodes, into the list as children


def ulist_to_html_node(block: str) -> ParentNode:   # Unordered list blocks should be surrounded by a <ul> tag, and each list item should be surrounded by a <li> tag.

    list_items = block.split("\n")

    html_items = [] 

    for item in list_items:

        text = item[ 2 : ]  # no need for splitting as with unordered list, they always have "- " at the start and cannot grow their beginning like orderded lists "100. "   # [2: ], 2 index to account for whitespace

        children = text_to_children(text)

        html_items.append (ParentNode("li", children) ) # Creating a Node for each item in the list # each list item should be surrounded by a <li> tag

    return ParentNode("ul", html_items)


def quote_to_html_node(block:str) -> ParentNode:   # Quote blocks should be surrounded by a <blockquote> tag.

    lines = block.split("\n")
    clean_lines = []

    for line in lines:

        if not line.startswith(">"):
            raise ValueError(f'invalid quote block: {block}')

        quote_stripped_line = line.lstrip(">")   # need to strip markdown quote blocks to get the text out

        text = quote_stripped_line.strip()      # need to strip whitespace to get the text out

        clean_lines.append(text) 

    cleaned_text = " ".join(clean_lines)   # need to join back together the cleaned list of text into a single line of text

    children = text_to_children(cleaned_text)  # calling helper function that turns this `text_filtered` into text nodes and then turns those text nodes into html nodes and returns those html nodes as a list of HTMLNodes 

    return ParentNode("blockquote", children)


# the "code" block is a bit of a special case: it should not do any inline markdown parsing of its children. I didn't use my text_to_children function for this block type, I manually made a TextNode and used text_node_to_html_node

def code_to_html_node(block:str) -> ParentNode:   # Code blocks should be surrounded by a <code> tag nested inside a <pre> tag.

    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError(f'invalid code block: {block}')
    
    text = block[4:-3]  # since code blocks are always starting and ending with "```", this allows access to just the text, no need for sanitizing new line characters here
                                        # !!! Not using helper function `text_to_children`, doing TextNode and HTMLNode creation with manual calls to other functions
    raw_text_node = TextNode(text, TextType.TEXT)   # creating manual raw TextNode 

    children = text_node_to_html_node(raw_text_node)  # inputing TextNodes to get out HTMLNode LeafNodes that are HTML formatted (HTMLNode) code blocks with proper html tags

    code = ParentNode( "code", [children] )   # Code blocks should be surrounded by a <code> tag 
    
    return ParentNode( "pre", [code])      # nested inside a <pre> tag.















# block_to_block_type USING more python keywords:
"""
def block_to_block_type(markdown: str):  # function that takes a single block of markdown text as input and returns the BlockType representing the type of block it is
                                                    # can assume all leading and trailing whitespace were already stripped 
    # HEADING
    if markdown.startswith("#"):

        heading_chars = markdown.split(" ", 1)[0]  # Headings start with 1-6 # characters, followed by a space and then the heading text.

        if (
            1 <= len(heading_chars) <= 6 
            and all (char == "#"  for char in heading_chars)
            and " " in markdown
        ):
            return BlockType.HEADING.value 

    # CODE
    if markdown.startswith("```\n") and markdown.endswith("```"): # Multiline Code blocks must start with 3 backticks and a newline, then end with 3 backticks.

        return BlockType.CODE 

    lines = markdown.split("\n")   # need to sanittize and filter out `\n` characters from input

    # QUOTES
    if all( line.startswith(">") for line in lines ):  # Every line in a quote block must start with a "greater-than" character: > followed by the quote text. 
                                                        # A space after > is allowed but not required.
        return BlockType.QUOTE

    # UNORDERED LIST

    if all( line.startswith("- ") for line in lines ): # Every line in an unordered list block must start with a - character, !!! followed by a space.

        return BlockType.UNORDERED_LIST 

    # ORDERED LIST 
                         # Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
    if all( 
        line.startswith(f"{i}. ") 
        for i, line in enumerate(lines, start=1) 
           ): 

        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH    # If none of the above conditions are met, the block is a normal paragraph.

"""
