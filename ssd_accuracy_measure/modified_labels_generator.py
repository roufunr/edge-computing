import json
import os


train_label_json_path = "/home/ubuntu/coco2017/annotations/instances_train2017.json"
val_label_json_path = "/home/ubuntu/coco2017/annotations/instances_val2017.json"


def load_from_json(json_path):
    with open(json_path, 'r') as json_file:
        # Load JSON data into a dictionary
        data = json.load(json_file)
    return data

def save_as_a_json(json_file_path, json_dict):
    with open(json_file_path, 'w') as json_file:
        json.dump(json_dict, json_file)


val_labels = load_from_json(val_label_json_path)

modified_labels = {}

category_dict = {}
for category in val_labels["categories"]:
    category_dict[category["id"]] = category["name"]


for label in val_labels["annotations"]:
    image_id = str(label["image_id"])
    image_id = "0" * (12 - len(image_id)) + image_id
    if image_id in modified_labels:
        modified_labels[image_id].append(category_dict[label["category_id"]])
    else: 
        modified_labels[image_id] = [category_dict[label["category_id"]]]

save_as_a_json("val_labels.json", modified_labels)



