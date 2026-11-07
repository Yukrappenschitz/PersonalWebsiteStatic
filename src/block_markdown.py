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

def markdown_to_html_node(markdown: str) -> list[HTMLNode]: #  converts a full markdown document into a single parent HTMLNode. 
                                     # That one parent HTMLNode should (obviously) contain many child HTMLNode objects representing the nested elements.
    
    blocks = markdown_to_blocks(markdown) # 1. Split the markdown into blocks (you already have a function for this)

    for block in blocks:  # 2. Loop over each block:

        type_block = block_to_block_type(block)   # 2.1 Determine the type of block (you already have a function for this) 

        match type_block:

            case BlockType.HEADING:
                helper_HEADING(block)

            case BlockType.PARAGRAPH:



def helper_HEADING(block: str) -> HTMLNode:

    return HTMLNode("p",block,None,None)






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
