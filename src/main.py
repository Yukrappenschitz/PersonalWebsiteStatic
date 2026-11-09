import os
import shutil
import sys 

from textnode import TextNode, TextType

from copy_static import copy_from_source_to_destination

from gencontent import generate_page, generate_pages_recursive

# Static Directory Path
dir_path_static = "./static"
# Destination Directory Path
dir_path_public = "./public"
# Content Directory Path
dir_path_content = "./content"

# Template HTML file path
template_path = "./template.html"


def main():

    # file content copying
    print(f'deleting public directory: {dir_path_public}')

    print(f'copying static files to public directory: {dir_path_static} -> {dir_path_public}')

    copy_from_source_to_destination(dir_path_static,dir_path_public)

    # page generation
    print("Generating pages...")         

    generate_pages_recursive(dir_path_content, template_path, dir_path_public)    # 2. should generate a page for every markdown file in the content directory and write the results to the public directory.



if __name__ == "__main__":
    main()







    
    """generate_page(
        os.path.join(dir_path_content, "index.md"), 
        template_path_html, 
        os.path.join(dir_path_public, "index.html")
        )"""

