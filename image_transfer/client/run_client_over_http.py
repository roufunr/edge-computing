import requests
import json
import time
from datetime import datetime 
import logging
logging.basicConfig(filename='clinet.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Create a logger
logger = logging.getLogger(__name__)

# Specify the URL of your Flask server
ip_addr = '192.168.1.174'
upload_url = f"http://{ip_addr}:5000/upload"  # Use an f-string
delete_entire_folder_url = f"http://{ip_addr}:5000/delete_all_images"

data_path = "/home/rouf-linux/single-frame-data"
compressed_data_path = data_path + "/compressed"
original_data_path = data_path + "/original"
result_path = "/home/rouf-linux/edge-computing/image_transfer/client/tx2i"
resolutions = {
    "cam1": ['160x90', '160x100', '160x120', '240x180', '320x180', '320x200', '320x240', '480x270', '480x300', '480x360', '640x360', '640x400', '640x480', '800x450', '800x500', '800x600', '1024x576', '1024x640', '1024x768', '1280x720', '1280x800', '1280x960', '1440x900', '1440x1080', '1920x1080'],
    "cam2": ['160x90', '160x100', '160x120', '240x180', '320x180', '320x200', '320x240', '480x270', '480x300', '480x360', '640x360', '640x400', '640x480', '800x450', '800x500', '800x600', '1024x576', '1024x640', '1024x768', '1280x720', '1280x800', '1280x960', '1440x900', '1440x1080', '1920x1080'],
    "cam3": ['160x90', '160x120', '176x144', '240x180', '320x180', '320x240', '480x270', '480x360', '640x360', '640x480', '800x450', '800x600', '1024x640', '1024x768', '1280x720', '1280x800', '1280x960'],
    "cam4": ['streamid_1/quality_1', 'streamid_1/quality_2', 'streamid_1/quality_3', 'streamid_1/quality_4', 'streamid_1/quality_5', 'streamid_0/quality_1', 'streamid_0/quality_2', 'streamid_0/quality_3', 'streamid_0/quality_4', 'streamid_0/quality_5']
}
total_experiment = 11
scaling_factors = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
ip_methods = ['INTER_NEAREST', 'INTER_LINEAR', 'INTER_CUBIC', 'INTER_AREA', 'INTER_LANCZOS4']
ip_methods_name_mapper = {
    'INTER_NEAREST': "Nearest",
    'INTER_LINEAR': "Linear",
    'INTER_CUBIC': "Cubic",
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
    total_data = 77 * len(ip_methods) * len(scaling_factors)
    completed_data = 0
    results = {}
    for cam in resolutions:
        for resolution in resolutions[cam]:
            for ip_method in ip_methods:
                for scaling_factor in scaling_factors: 
                    image_files = []
                    image_name = "0.jpeg" if cam == "cam4" else "0.bmp"
                    key = cam + "/" + resolution + "/" + ip_method + "/" + str(scaling_factor)
                    image_absolute_path = compressed_data_path + "/" + key + "/" + image_name
                    image_files.append(("images", (image_name, open(image_absolute_path, 'rb'))))
                    start_time = time.time() * 1000
                    key = "compressed/" + key
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
                    logger.info(str(exp_id)  + "-> " + "Compressed image transfer DONE ::::" + str((completed_data / total_data) * 100) + "%")
    return results

def transfer_original_image(exp_id):
    total_data = 77
    completed_data = 0
    results = {}
    for cam in resolutions:
        for resolution in resolutions[cam]:
            image_files = []
            image_name = "0.jpeg" if cam == "cam4" else "0.bmp"
            key = cam + "/" + resolution
            image_absolute_path = original_data_path + "/" + key + "/" + image_name
            image_files.append(("images", (image_name, open(image_absolute_path, 'rb'))))
            start_time = time.time() * 1000
            key = "original/" + key
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
            logger.info(str(exp_id)  + "-> " + "Original image transfer DONE ::::" + str((completed_data / total_data) * 100) + "%")
    return results


def delete_all_images(): 
    try:
        response = requests.post(delete_entire_folder_url)
        if response.status_code == 200:
            logger.info("All images deleted successfully")
        else:
            logger.info("Failed to delete images:" + response.json())
    except requests.exceptions.RequestException as e:
        logger.info("Request failed:")

for i in range(1): 
    # compressed_result = transfer_compressed_image(i)
    origianl_result = transfer_original_image(i)
    # result = {
    #     "compressed": compressed_result,
    #     "original": origianl_result
    # }
    # save_data_as_json(result, result_path + "/" + str(i) + ".json")
    # delete_all_images()
    # time.sleep(30)

