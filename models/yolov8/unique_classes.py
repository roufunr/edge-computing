import json

# Open the JSON file
with open('labels.json', 'r') as file:
    # Load the JSON data into a Python dictionary
    data_dict = json.load(file)

unique_classes = []

for image in data_dict:
    for object in image['objects']:
        name = object['name']
        if name in unique_classes:
            continue
        else:
            unique_classes.append(name)

#print(unique_classes)
class_idx = [66, 56, 60, 59, 62, 63, 6, 28, 7, 0, 72, 37, 68, 31, 36, 8]
unique_class_map = {}
for i in range(len(unique_classes)):
    unique_class_map[unique_classes[i]] = class_idx[i]

for image in data_dict:
    for object in image['objects']:
        name = object['name']
        object['idx'] = unique_class_map[name]

json_labels = json.dumps(data_dict, indent=2)

# Write JSON to a file
json_file_path = "./labels_with_index.json"
with open(json_file_path, 'w') as json_file:
    json_file.write(json_labels)

print(f"Labels saved to: {json_file_path}")

#print(unique_class_map)
# ['keyboard', 'chair', 'dining table', 'bed', 'tv', 'laptop', 'train', 'suitcase', 'truck', 'person', 'refrigerator', 'surfboard', 'microwave', 'snowboard', 'skateboard', 'boat']
# [66, 56, 60, 59, 62, 63, 6, 28, 7, 0, 72, 37, 68, 31, 36, 8]




