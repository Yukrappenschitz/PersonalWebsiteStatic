import os
import shutil


def copy_from_source_to_destination_r(source_dir_path: str, destination_dir_path:str):  # a recursive helper function that copies all the contents from a source directory to a destination directory (in our case, static to public)

    if not os.path.exists(destination_dir_path):
        print(f'creating directory: {destination_dir_path}')    # leaving traces just to keep the bad juju away from recursive functions that interact directly with the filesystem in THE Project itself
        os.makedirs(destination_dir_path)

    for file_name in os.listdir(source_dir_path):
        source_path = os.path.join(source_dir_path, file_name)
        destination_path = os.path.join(destination_dir_path, file_name)
        
        if os.path.isfile(source_path):
            print(f'copying file: {source_path} -> {destination_path}')        # leaving traces just to keep the bad juju away from recursive functions that interact directly with the filesystem in THE Project itself
            shutil.copy(source_path, destination_path)
        
        else:                                 # if we hit a directory in the source, need to make that same directory in the destination_dir and THEN call the recursive function

            copy_from_source_to_destination_r(source_path, destination_path)


def copy_from_source_to_destination(source_dir_path: str, destination_dir_path: str): # 2. a recursive function that copies all the contents from a source directory to a destination directory (in our case, static to public) 

    try:
        # source_dir path verification
        is_valid_path_source: bool = os.path.exists(source_dir_path)

        if is_valid_path_source == False:
            raise Exception(f'error: invalid path supplied: {source_dir_path}')
        
        if os.path.exists(destination_dir_path): # 2.a It should first delete all the contents of the destination directory (public) to ensure that the copy is clean.
        
            shutil.rmtree(destination_dir_path)   # !!! removing ALL content from destination_dir

        os.mkdir(destination_dir_path)     # RECREATING THE DELETED destination_dir

        # recursive copy function call

        copy_from_source_to_destination_r(source_dir_path , destination_dir_path)   # It should copy all files and subdirectories, nested files, etc.
        

    except Exception as e:
        raise FileExistsError(f'{e}')


