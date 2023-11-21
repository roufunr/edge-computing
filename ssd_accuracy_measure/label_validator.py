import os
import json

val_img_path = "/home/ubuntu/coco2017/val2017"
file_names = os.listdir(val_img_path)

def load_from_json(json_path):
    with open(json_path, 'r') as json_file:
        # Load JSON data into a dictionary
        data = json.load(json_file)
    return data

def save_as_a_json(json_file_path, json_dict):
    with open(json_file_path, 'w') as json_file:
        json.dump(json_dict, json_file)


labels = load_from_json("/home/ubuntu/edge-computing/ssd_accuracy_measure/val_labels.json")

valid_labels = {}
for filename in file_names:
    if filename.split(".")[0] not in labels:
        print("file: " + filename + " is missing in label json")
        continue

    valid_labels[filename.split(".")[0]] = labels[filename.split(".")[0]]

save_as_a_json("valid_labels.json", valid_labels)
print("Total Valid labels: " + str(len(valid_labels)))