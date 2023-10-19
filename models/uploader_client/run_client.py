import requests
import json
from time import time
from datetime import datetime  # Import datetime module

# Specify the URL of your Flask server
ip_addr = '192.168.1.194'
upload_url = f"http://{ip_addr}:5000/upload"  # Use an f-string

data_path = "./../data"
result_path = "./result/orin"

with open(data_path + '/labels.json', 'r') as json_file:
    labels = json.load(json_file)

modified_labels = {}
for label in labels:
    path = label['image_path']
    image_name = path.split("/")[-1]
    dir_path = path.replace(image_name, "")
    if dir_path in modified_labels:
        modified_labels[dir_path].append(image_name)
    else:
        modified_labels[dir_path] = [image_name]

for i in range(10+1): 
    total_data = len(labels)
    completed_data = 0
    results = {}
    for key in modified_labels:
        image_files = []
        images_path = key
        for image_name in modified_labels[key]:
            image_files.append(("images", (image_name, open(data_path + key + image_name, 'rb'))))
        start_time = time() * 1000
        data = {'path': images_path, 'transfer_start_time': start_time}
        response = requests.post(upload_url, files=image_files, data=data)  # Simplify request
        end_time = time() * 1000
        response_time = end_time - start_time
        response_data = response.json()
        results[key] = {
            "transfer_time": response_data["transfer_time"],
            "disk_write_time": response_data["disk_write_time"],
            "response_time": response_time
        }
        completed_data += len(image_files)
        print(str(i)  + "-> ""DONE", ((completed_data / total_data) * 100), "%")

    json_results = json.dumps(results, indent=2)
    date_time = datetime.utcfromtimestamp(time()).strftime('%Y%m%d_%H:%M:%S_utc')
    result_json_name = f'exp_{i}_client_side_transfer_time_{date_time}.json'  # Use an f-string
    with open(result_path + '/' + result_json_name, 'w') as json_file:
        json_file.write(json_results)

