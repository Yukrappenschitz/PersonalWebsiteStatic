import os
import shutil

from textnode import TextNode, TextType

from copy_static import copy_from_source_to_destination

from gencontent import generate_page

# Source Directory Path
dir_path_static = "./static"
# Destination Directory Path
dir_path_public = "./public"

# GENERATING PAGES
dir_path_content = "./content"
template_path_html = "./template.html"


def main():

    # file content copying
    print(f'deleting public directory: {dir_path_public}')

    print(f'copying static files to public directory: {dir_path_static} -> {dir_path_public}')

    copy_from_source_to_destination(dir_path_static,dir_path_public)

    # page generation
    print("Generating page...")         
    
    generate_page(
        os.path.join(dir_path_content, "index.md"), 
        template_path_html, 
        os.path.join(dir_path_public, "index.html")
        )



if __name__ == "__main__":
    main()








