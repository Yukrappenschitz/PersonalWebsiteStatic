import os 
import shutil
import pathlib

from markdown_blocks import (
    BlockType,
    markdown_to_blocks, 
    block_to_block_type, 
    markdown_to_html_node, 
)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    list_entry_dir = os.listdir(dir_path_content)

    for entry in list_entry_dir:
        from_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path,entry)
        
        if os.path.isfile(from_path):

            if from_path.endswith(".md"):

                dest_path_html = os.path.splitext(dest_path)[0] + ".html"   # need to strip .md file extension and replace with .html

                generate_page(from_path, template_path, dest_path_html)
            
        else:
            generate_pages_recursive( 
                            from_path,
                            template_path, 
                            dest_path
                            )
            
    



def generate_page(from_path: str, template_path: str, dest_path: str):      # 5.Create a generate_page(from_path, template_path, dest_path) function.

    generating_message = f'Generating page from {from_path} to {dest_path} using {template_path}'
    print(generating_message)

    with (
        open(from_path, "r") as source,
        open(template_path, "r") as template
    ):     
        source_markdown = source.read()         # 5.2 Read the markdown file at from_path and store the contents in a variable.
        template_html = template.read()             # 5.3 Read the template file at template_path and store the contents in a variable.
                                                    # # storing the read file as a long asz string in the variable names (`source_markdown` and `template_html`) so no need to keep the actual files open
        source.close()                       # redundant close, since python `with` keyword closes after the block is finished running
        template.close()                      

    # Markdown to HTML conversion
    HTML_nodes = markdown_to_html_node(source_markdown)    # 5.4 Use markdown_to_html_node function and 
    HTML_string = HTML_nodes.to_html()                    # .to_html() method to convert the markdown file to an HTML string.
    Content = HTML_string

    Title = extract_title(source_markdown)              # 5.5 Use the extract_title function to grab the title of the page 
    
    # Title and content injection like the best medical grade morphine stolen from a truck run that the driver was definitely involved in but now the driver lives in a cave after being betrayed by the dealers that actually stole them heavenly juice
    page = template_html.replace( "{{ Title }}", Title )      # 5.6 Replace the {{ Title }} and {{ Content }} placeholders in the template with the HTML and title you generated.
    page = page.replace("{{ Content }}", Content) 
    
    
    dest_dir_path = os.path.dirname(dest_path)   # just getting the directory path of the file since we are supplied a path relative to the root of the project  
    
        # boring asz dir creation if no dir is there since the function expects a path from the root of the project to the desired destination dir
    if dest_dir_path != '':                    # os.path.dirname returns everything before the last / in a path, and it returns an empty string when the path has no directory part
        os.makedirs(dest_dir_path, exist_ok=True)             # the main function will provide the actual file name
    
    with open(dest_path, "w") as to_file:
        to_file.write(page)
        
        to_file.close()                  # redundant close since python keyword `with` takes care of closing the file after block is finished running but kept in to waste time typing extra words cause bored and its late
    

def extract_title(markdown: str) -> str:   # It should pull the h1 header from the markdown file (the line that starts with a single #) and return it.
    lines = markdown.split("\n")
    
    for line in lines:       # just using \n characters to split up the whole markdown document into sections
        
        if line.startswith("# "):          # this approach accounts for the fact that there can be empty spaces before the title 
            Title = line[2 : ]               
            return Title
                
    raise ValueError(f'invalid markdown syntax: no title found (h1 header)')



