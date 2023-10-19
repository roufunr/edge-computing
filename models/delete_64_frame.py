import shutil
import os

def delete_folder_recursive(root_folder):
    for root, dirs, files in os.walk(root_folder, topdown=False):
        for dir_name in dirs:
            if dir_name == '64':
                folder_path = os.path.join(root, dir_name)
                try:
                    print(f"Deleting folder and its contents: {folder_path}")
                    shutil.rmtree(folder_path)
                except Exception as e:
                    print(f"Error deleting folder {folder_path}: {str(e)}")


delete_folder_recursive('./data_32')
