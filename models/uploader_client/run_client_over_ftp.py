import requests
import subprocess
import json
import time
from datetime import datetime  # Import datetime module
import paramiko

# Specify the URL of your Flask server
ip_addr = '192.168.1.194'
upload_url = f"http://{ip_addr}:5000/upload"  # Use an f-string

data_path = "/home/rouf-linux/data/data_32"
result_path = "/home/rouf-linux/edge-computing/models/uploader_client/result/orin"
user = "orin"
ftp_destination_machine = f'{user}@{ip_addr}:'


def delete_all_data_on_server(): 
    # SSH connection parameters
    hostname = '192.168.1.194'  # Replace with the remote server's IP address or hostname
    username = 'orin'  # Replace with your SSH username
    remote_dir = '~/data_dir/*'
    ssh_command = f'ssh {username}@{hostname} "rm -rf {remote_dir}"'
    subprocess.run(ssh_command, shell=True)
    print(f"Remote directory '{remote_dir}' deleted.")



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
        
        images_path = key
        destination_key = key.replace(key.split("/")[-2] + "/", "")
        source_dir = data_path + key
        destination_dir = ftp_destination_machine + "~/data_dir/"
        print(source_dir + " ---> " + destination_dir)
        start_time = time.time() * 1000
        for image in modified_labels[key]:
            new_image = (key + image).replace("/", "_")
            subprocess.call(['scp', source_dir + image, destination_dir + new_image])
        end_time = time.time() * 1000
        transfer_time = end_time - start_time
        results[key] = {
            "transfer_time": transfer_time,
        }
        completed_data += len(modified_labels[key])
        print(str(i)  + "-> ""DONE", ((completed_data / total_data) * 100), "%")

    
        


    json_results = json.dumps(results, indent=2)
    date_time = datetime.utcfromtimestamp(time.time()).strftime('%Y%m%d_%H:%M:%S_utc')
    result_json_name = f'exp_{i}_client_side_transfer_time_{date_time}.json'  # Use an f-string
    with open(result_path + '/' + result_json_name, 'w') as json_file:
        json_file.write(json_results)

    print("client goes to sleep for 2 min!")
    time.sleep(30)
    delete_all_data_on_server()
    time.sleep(30)
    subprocess.call(['scp','-r', '/home/rouf-linux/data/data_dir', ftp_destination_machine + "~/"])
    time.sleep(30)


