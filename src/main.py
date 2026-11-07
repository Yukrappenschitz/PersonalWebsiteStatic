import os
import shutil
from textnode import TextNode, TextType



def copy_from_source_to_destination(source_dir: str, destination_dir: str):

    try:
        # dir path verification
        is_valid_path_source: bool = os.path.exists(source_dir)
        is_valid_path_destination: bool = os.path.exists(destination_dir)

        if is_valid_path_source == False or is_valid_path_destination == False:
            raise Exception("error: invalid directory path supplied")

                                                    # It should first delete all the contents of the destination directory (public) to ensure that the copy is clean.
        # !!! removing ALL content from destination_dir
        shutil.rmtree(destination_dir)

        # RECREATING THE DELETED destination_dir
        os.mkdir(destination_dir)



        
    except Exception as e:
        return f'Error: {type(e).__name__} - {e}'


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



def main():

    test_text = TextNode("testing", TextType.TEXT,)
    test_link = TextNode("testing", TextType.LINK, "mahnuhtsachk")

    print(test_text, test_link)

main()


