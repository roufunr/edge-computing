import os

def search_files(directory, extensions):
    starting_directory = "/home/rouf-linux/Documents/codes/image_acquisition/results/data"
    file_extensions = ('.jpeg', '.bmp')
    images_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(extensions):
                file_path = os.path.abspath(os.path.join(root, file))
                images_list.append(file_path)
                print(file_path)
    return images_list




