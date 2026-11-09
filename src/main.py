
from textnode import TextNode, TextType

from copy_static import copy_from_source_to_destination

from generate_page import generate_page

# Source Directory Path
dir_path_static = "./static"

# Destination Directory Path
dir_path_destination = "./public"


# GENERATING PAGES
from_path = "content/index.md"
template_html = "template.html"
dest_path = "public/index.html"



def main():

    print(f'deleting public directory: {dir_path_destination}')

    print(f'copying static files to public directory: {dir_path_static} -> {dir_path_destination}')

    copy_from_source_to_destination(dir_path_static,dir_path_destination)

    generate_page(from_path, template_html, dest_path)




main()





"""
        abs_source_dir: str = os.path.abspath(source_dir)
        abs_destination_dir: str = os.path.abspath(destination_dir) 

        norm_abs_source_dir: str = os.path.normpath(abs_source_dir)
        norm_abs_destination_dir: str = os.path.normpath(abs_destination_dir)

        is_dir_source_dir:bool = os.path.isdir(norm_abs_source_dir)
        is_dir_destination_dir: bool = os.path.isdir(norm_abs_destination_dir)

        if is_dir_destination_dir == False or is_dir_source_dir == False:
            return f'error: given directory file paths are not directories. source: {source_dir}, destination: {destination_dir}'

"""





