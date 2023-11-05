import os
import json

raw_results_base_path = "/Users/abdurrouf/edge-computing/image_transfer/report_generation/raw_results"
parts = ["compression", "decompression", "transfer"]
transfer_image_type = ["original", "compressed"]
resolutions = ['160x90', '160x100', '160x120', '320x180', '320x200', '320x240', '480x270', '480x300', '480x360', '640x360', '640x400', '640x480', '800x450', '800x500', '800x600', '1024x576', '1024x640', '1024x768', '1280x720', '1280x800', '1280x960', '1440x900', '1440x1080', '1920x1080']
frames = [1, 2, 4, 8, 16, 32]
total_experiment = 10
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

def load_json(json_path):
    with open(json_path, 'r') as json_file:
        json_data = json.load(json_file)
    return json_data

def generateKeys(exp_id, image_type):
    keys = []
    if image_type == "original":
        for resolution in resolutions:
            for frame in frames:
                keys.append(str(exp_id) + "/" + resolution + "/" + frame)
    else: 
        for ip_method in ip_methods:
            for scaling_factor in scaling_factors:
                for resolution in resolutions:
                    for frame in frames:
                        keys.append(str(exp_id) + "/" + ip_method + "/" + str(scaling_factor) + "/" + resolution + "/" + str(frame))
    return keys



def load_data():
    data = {}
    for part in parts:
        part_data = []
        for i in range(total_experiment):
            json_path = raw_results_base_path + "/" + part + "/" + str(i + 1) + ".json"
            part_data.append(load_json(json_path))
        data[part] = part_data
    return data

def rearrange_data_vertically(data):
    v_data = {}
    for part in parts:
        if part == "transfer":
            v_keys = {
                "original": 
            }

        

