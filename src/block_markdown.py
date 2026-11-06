
from textnode import TextNode, TextType 

def markdown_to_blocks(markdown: str) -> list[str] :   # It takes a raw Markdown string (representing a full document) as input and returns a list of "block" strings. 

    split_blocks = markdown.split("\n\n")  #  used to split a string into blocks based on a delimiter (\n\n is a double newline).

    filtered_blocks = []

    for block in split_blocks:    # need to iterate over all blocks to clean and sanitize whitespaces and empty blocks
        
        block = block.strip()  # should .strip() any leading or trailing whitespace from each block.

        if block != '':        # Remove any "empty" blocks due to excessive newlines.
            filtered_blocks.append(block)
            
    return filtered_blocks 

