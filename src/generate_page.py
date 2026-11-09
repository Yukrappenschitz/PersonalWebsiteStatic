import os 
import shutil

from markdown_blocks import (
    BlockType,
    markdown_to_blocks, 
    block_to_block_type, 
    markdown_to_html_node, 
)

def extract_title(markdown: str) -> str:   # It should pull the h1 header from the markdown file (the line that starts with a single #) and return it.

    if not markdown.startswith("# "):
        raise Exception(f'invalid markdown syntax: no title (h1 header)')
    
    stripped_header = markdown[2: ]

    clean_header = stripped_header.strip()

    return clean_header 

def generate_page(from_path: str, template_path: str, dest_path: str):      # 5.Create a generate_page(from_path, template_path, dest_path) function.

    generating_message = f'Generating page from {from_path} to {dest_path} using {template_path}'
    print(generating_message)

    with (
        open(from_path, "r") as source,
        open(template_path, "r") as template
    ):     
        source_markdown = source.read()         # 5.2 Read the markdown file at from_path and store the contents in a variable.
        template_html = template.read()             # 5.3 Read the template file at template_path and store the contents in a variable.

        HTML_nodes = markdown_to_html_node(source_markdown)    # 5.4 Use markdown_to_html_node function and 
        HTML_string = HTML_nodes.to_html()                    # .to_html() method to convert the markdown file to an HTML string.

        Title = extract_title(HTML_string)              # 5.5 Use the extract_title function to grab the title of the page 
        Content = HTML_string.split(f'# {Title}')[1]
        
        HTML_title = template_html.replace( "{{ Title }}", Title )      # 5.6 Replace the {{ Title }} and {{ Content }} placeholders in the template with the HTML and title you generated.
        HTML_finished = HTML_title.replace("{{ Content }}", Content) 


    destination_path = os.path.dirname(dest_path) 

    if not os.path.exists(destination_path):
        os.makedirs(dest_path)
    
    with open(f'{destination_path}/test.html', "w") as test_file:
        test_file.write(HTML_finished)
    


