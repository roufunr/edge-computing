import requests
import json
import time
from datetime import datetime  # Import datetime module

# Specify the URL of your Flask server
ip_addr = '54.67.31.203'
upload_url = f"http://{ip_addr}:5000/upload"  # Use an f-string

data_path = "/home/rouf-linux/data/data_32"
result_path = "/home/rouf-linux/edge-computing/models/uploader_client/result/cloud_virginia"


def delete_all_data_on_server(): 
    # Endpoint to delete all images
    delete_images_endpoint = f'http://{ip_addr}:5000/delete_all_images'
    try:
        response = requests.post(delete_images_endpoint)
        if response.status_code == 200:
            print('All images deleted successfully.')
        else:
            print('Failed to delete images. Server response:', response.status_code)
    except Exception as e:
        print('An error occurred:', str(e))


        
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
        start_time = time.time() * 1000
        data = {'path': images_path, 'transfer_start_time': start_time}
        response = requests.post(upload_url, files=image_files, data=data)  # Simplify request
        end_time = time.time() * 1000
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
    date_time = datetime.utcfromtimestamp(time.time()).strftime('%Y%m%d_%H:%M:%S_utc')
    result_json_name = f'exp_{i}_client_side_transfer_time_{date_time}.json'  # Use an f-string
    with open(result_path + '/' + result_json_name, 'w') as json_file:
        json_file.write(json_results)
    
    print("client goes to sleep for 30 sec!")
    time.sleep(10)
    delete_all_data_on_server()
    time.sleep(20)


