import os
import shutil
import json

# Define the source path where the images are located
source_path = "/home/rouf-linux/Documents/codes/image_acquisition/results/data"

# Define the destination folder
destination_folder = "test_data"

# Create the destination folder if it doesn't exist
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# List of image paths to be copied
image_paths = [
    "/p3265_axis_20231009_223413/1280x800/8/12.bmp",
    "/p3265_axis_20231009_223413/1280x800/8/10.bmp",
    "/p3265_axis_20231009_223413/1024x640/8/9.bmp",
    "/p3265_axis_20231009_223413/800x450/8/9.bmp",
    "/p3364_axis_20231009_214248/1280x800/8/13.bmp",
    "/p3364_axis_20231009_214248/160x90/64/120.bmp",
    "/vivotek_20231009_201139/streamid_0/quality_3/64/115.jpeg",
    "/vivotek_20231009_201139/streamid_1/quality_3/16/20.jpeg",
    "/p3245_axis_20231010_020941/800x450/8/9.bmp",
    "/p3245_axis_20231010_020941/800x450/64/87.bmp",
    "/p3245_axis_20231010_020941/480x270/32/44.bmp",
    "/p3245_axis_20231010_020941/1920x1080/8/13.bmp"
]

# Copy each image to the destination folder
for image_path in image_paths:
    full_source_path = source_path + image_path
    destination_path = destination_folder + image_path
    path = destination_path.replace(destination_path.split('/')[-1], '')
    os.makedirs(path, exist_ok=True)
    shutil.copy(full_source_path, path)

print("Images copied to the test_data folder.")

data_dict = {}


# Open the JSON file
with open('labels_with_index.json', 'r') as file:
    # Load the JSON data into a Python dictionary
    data_dict = json.load(file)


test_labels = []
for image in data_dict:
    image_path = image['image_path']
    for path in image_paths:
        if path == image_path:
            test_labels.append(image)

json_labels = json.dumps(test_labels, indent=2)

# Write JSON to a file
json_file_path = "./" + destination_folder+ "/test_labels.json"
with open(json_file_path, 'w') as json_file:
    json_file.write(json_labels)

print(f"Labels saved to: {json_file_path}")

