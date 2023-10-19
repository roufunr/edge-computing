import json
json_data = []
with open('./data_64/labels.json', 'r') as file:
    json_data = json.load(file)

new_json = []
for data in json_data:
    image_path = data['image_path']
    pieces = image_path.split("/")
    if pieces[len(pieces) - 2] != "64":
        new_json.append(data)

print("prev", len(json_data))
print("now", len(new_json))
# new_json_data = json.dumps(new_json, indent=2)
# with open('./data_64/labels.json', 'w') as json_file:
#     json_file.write(new_json_data)