import requests
import json
import time
from datetime import datetime  # Import datetime module

# Specify the URL of your Flask server
ip_addr = '3.214.216.88'
upload_url = f"http://{ip_addr}:5000/upload"  # Use an f-string

data_path = "/home/rouf-linux/data"
compressed_data_path = data_path + "/compressed"
original_data_path = data_path + "/original"
result_path = "/home/rouf-linux/edge-computing/image_transfer/client/result"

resolutions = ['160x90', '160x100', '160x120', '320x180', '320x200', '320x240', '480x270', '480x300', '480x360', '640x360', '640x400', '640x480', '800x450', '800x500', '800x600', '1024x576', '1024x640', '1024x768', '1280x720', '1280x800', '1280x960', '1440x900', '1440x1080', '1920x1080']
frames = [1, 2, 4, 8, 16, 32]
total_experiment = 1
scaling_factors = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
ip_methods = ['INTER_NEAREST', 'INTER_LINEAR', 'INTER_CUBIC', 'INTER_AREA', 'INTER_LANCZOS4']
ip_methods_name_mapper = {
    'INTER_NEAREST': "Nearest",
    'INTER_LINEAR': "Linear",
    'INTER_CUBIC': "Inter-Cubic",
    'INTER_AREA': "Area",
    'INTER_LANCZOS4': "Lanczos4"
}


def save_data_as_json(data, json_path):
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


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


def transfer_compressed_image(exp_id):
    total_data = len(ip_methods) * len(scaling_factors) * len(resolutions) * ((2**6) - 1)
    completed_data = 0
    results = {}
    
    for ip_method in ip_methods:
        for scaling_factor in scaling_factors:
            for resolution in resolutions:
                for frame in frames:
                    first_image_idx = frame - 1
                    image_files = []
                    image_relative_path = ip_method + "/" + str(scaling_factor) + "/" + resolution + "/" + str(frame)
                    for i in range(frame):
                        image_name = str(first_image_idx + i) + ".bmp"
                        image_absolute_path = compressed_data_path + "/" + image_relative_path + "/" + image_name
                        image_files.append(("images", (image_name, open(image_absolute_path, 'rb'))))
                    start_time = time.time() * 1000
                    key = str(exp_id) + "/compressed/" +  ip_method + "/" + str(scaling_factor) + "/" + resolution + "/" + str(frame)
                    data = {'path': key, 'transfer_start_time': start_time}
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
                    print(str(exp_id)  + "-> " + "Compressed image transfer DONE", ((completed_data / total_data) * 100), "%")
    return results

def transfer_original_image(exp_id):
    total_data = len(resolutions) * ((2**6) - 1)
    completed_data = 0
    results = {}
    
    
    for resolution in resolutions:
        for frame in frames:
            first_image_idx = frame - 1
            image_files = []
            image_relative_path = resolution + "/" + str(frame)
            for i in range(frame):
                image_name = str(first_image_idx + i) + ".bmp"
                image_absolute_path = original_data_path + "/" + image_relative_path + "/" + image_name
                image_files.append(("images", (image_name, open(image_absolute_path, 'rb'))))
            start_time = time.time() * 1000
            key = str(exp_id) + "/original/" +  resolution + "/" + str(frame)
            data = {'path': key, 'transfer_start_time': start_time}
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
            print(str(exp_id)  + "-> ""DONE", ((completed_data / total_data) * 100), "%")
    return results



for i in range(total_experiment): 
    compressed_result = transfer_compressed_image(i)
    # origianl_result = transfer_original_image(i)
    # result = {
    #     "compressed": compressed_result,
    #     "original": origianl_result
    # }

    # save_data_as_json(result, "/home/rouf-linux/edge-computing/image_transfer/client/result/" + str(i) + ".json")

