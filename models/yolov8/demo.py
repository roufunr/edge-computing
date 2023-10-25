from PIL import Image
from ultralytics import YOLO
import os
import json

def get_all_images_list(starting_directory, file_extensions):
    images_list = []
    for root, dirs, files in os.walk(starting_directory):
        for file in files:
            if file.lower().endswith(file_extensions):
                file_path = os.path.abspath(os.path.join(root, file))
                images_list.append(file_path)
                #print(file_path)
    return images_list

def label_the_image(image_path, model): 
    results = model(image_path)  # results list
    for result in results:
        im_array = result.plot()  # plot a BGR numpy array of predictions
        im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image

        new_image_path = image_path.replace('data', 'labeled_data')
        new_image_dir = os.path.dirname(new_image_path)

        # Create directories if they don't exist
        os.makedirs(new_image_dir, exist_ok=True)

        im.save(new_image_path)  # save image

        boxes = result.boxes  # Boxes object for bbox outputs
        classes = boxes.cls.numpy().tolist()
        xyxys = boxes.xyxy.numpy().tolist()
        xywhs = boxes.xywh.numpy().tolist()
        conf = boxes.conf.numpy().tolist()
        names_list = result.names
        number_of_objects = len(classes)

        label = {}
        label['image_path'] = image_path.replace('/home/rouf-linux/Documents/codes/image_acquisition/results/data', '')
        label['objects'] = []
        for i in range(number_of_objects):
            object = {
                'name': names_list[classes[i]],
                'position': {
                    'xyxy': {
                        'xy_0': [xyxys[i][0], xyxys[i][1]],
                        'xy_1': [xyxys[i][2], xyxys[i][3]],
                    },
                    'xywh': {
                        'xy': [xywhs[i][0], xywhs[i][1]],
                        'w': xywhs[i][2],
                        'h': xywhs[i][3]
                    }
                },
                'confidence': conf[i]
            }
            label['objects'].append(object)

    return label

# Initialize YOLO model
model = YOLO('yolov8n.pt')

# Specify the starting directory and file extensions
starting_directory = "/home/rouf-linux/Documents/codes/image_acquisition/results/data"
file_extensions = ('.jpeg', '.bmp')

# Get the list of image paths
images_path_list = get_all_images_list(starting_directory, file_extensions)

# Process images and generate labels
labels = []
for image_path in images_path_list:
    label = label_the_image(image_path, model)
    labels.append(label)
    print(image_path, "DONE")

# Convert labels to JSON
json_labels = json.dumps(labels, indent=2)

# Write JSON to a file
json_file_path = "./labels.json"
with open(json_file_path, 'w') as json_file:
    json_file.write(json_labels)

print(f"Labels saved to: {json_file_path}")
