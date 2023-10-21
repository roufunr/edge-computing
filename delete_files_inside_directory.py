import os

def delete_files_in_directory(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)

directory_path = '/home/rouf-linux/data/data_dir'
delete_files_in_directory(directory_path)
