import os
import shutil
from textnode import TextNode, TextType


def copy_from_source_to_destination_r(source_dir: str, destination_dir:str):  # a recursive helper function that copies all the contents from a source directory to a destination directory (in our case, static to public)

    for name in os.listdir(source_dir):
        source_path = os.path.join(source_dir, name)
        destination_path = os.path.join(destination_dir, name)

        if os.path.isfile(source_path):
            print(f'copying file: {source_path}')
            shutil.copy(source_path, destination_path)
        
        else:                                 # if we hit a directory in the source, need to make that same directory in the destination_dir and THEN call the recursive function
            print(f'creating directory: {destination_path}')
            os.makedirs(destination_path)

            copy_from_source_to_destination_r(source_path, destination_path)


def copy_from_source_to_destination(source_dir: str, destination_dir: str): # 2. a recursive function that copies all the contents from a source directory to a destination directory (in our case, static to public) 

    try:
        # source_dir path verification
        is_valid_path_source: bool = os.path.exists(source_dir)

        if is_valid_path_source == False:
            raise Exception(f'error: invalid path supplied: {source_dir}')
        
        if os.path.exists(destination_dir): # 2.a It should first delete all the contents of the destination directory (public) to ensure that the copy is clean.
        
            shutil.rmtree(destination_dir)   # !!! removing ALL content from destination_dir

        os.mkdir(destination_dir)     # RECREATING THE DELETED destination_dir

        # recursive copy function call

        copy_from_source_to_destination_r(source_dir , destination_dir)   # It should copy all files and subdirectories, nested files, etc.
        

    except Exception as e:
        raise FileExistsError(f'{e}')




def main():
    copy_from_source_to_destination("invalid_source","invalid_destination")

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





