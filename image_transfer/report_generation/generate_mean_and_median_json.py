import os
import json

raw_results_base_path = "/home/rouf-linux/edge-computing/image_transfer/report_generation/raw_results"
parts = ["compression", "decompression", "transfer"]
transfer_image_type = ["original", "compressed"]
transfer_time_type = ["transfer_time", "disk_write_time", "response_time"]
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

def generateKeys(image_type):
    keys = []
    if image_type == "original":
        for resolution in resolutions:
            for frame in frames:
                keys.append(resolution + "/" + str(frame))
    else: 
        for ip_method in ip_methods:
            for scaling_factor in scaling_factors:
                for resolution in resolutions:
                    for frame in frames:
                        keys.append(ip_method + "/" + str(scaling_factor) + "/" + resolution + "/" + str(frame))
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
            v_data["transfer"] = {
                "original": {key:{timeKey:[] for timeKey in transfer_time_type} for key in generateKeys("original")},
                "compressed": {key:{timeKey:[] for timeKey in transfer_time_type} for key in generateKeys("compressed")}
            }
            
            for image_type in transfer_image_type:
                keys = v_data["transfer"][image_type]
                for key in keys:
                    for timeKey in transfer_time_type:
                        for i in range(total_experiment):
                            v_data["transfer"][image_type][key][timeKey].append(data["transfer"][i][image_type][key][timeKey])      
        else: 
            print(part)
            v_data[part] = {key:[] for key in generateKeys("compressed")}
            keys = v_data[part]
            for key in keys:
                for i in range(total_experiment):
                    v_data[part][key].append(data[part][i][key])
    return v_data

def calculate_average(v_data): 
    avg_data = {}
    for part in parts:
        if part == "transfer":
            avg_data["transfer"] = {
                "original": {key:{timeKey: 0 for timeKey in transfer_time_type} for key in generateKeys("original")},
                "compressed": {key:{timeKey: 0 for timeKey in transfer_time_type} for key in generateKeys("compressed")}
            }
            
            for image_type in transfer_image_type:
                keys = v_data["transfer"][image_type]
                for key in keys:
                    for timeKey in transfer_time_type:
                        sum = 0
                        for i in range(total_experiment):
                            sum += v_data["transfer"][image_type][key][timeKey][i]
                        avg_data["transfer"][image_type][key][timeKey] = sum / total_experiment 
        else:
            avg_data[part] = {key: 0 for key in generateKeys("compressed")}
            keys = v_data[part]
            for key in keys:
                sum = 0
                for i in range(total_experiment):
                    sum += v_data[part][key][i]
                avg_data[part][key] = sum / total_experiment
    return avg_data 

def get_median(lst):
    sorted_lst = sorted(lst)
    n = len(sorted_lst)
    if n % 2 == 0:
        mid1 = sorted_lst[n // 2 - 1]
        mid2 = sorted_lst[n // 2]
        median = (mid1 + mid2) / 2.0
    else:
        median = sorted_lst[n // 2]
    return median

    
def calculate_median(v_data): 
    median_data = {}
    for part in parts:
        if part == "transfer":
            median_data["transfer"] = {
                "original": {key:{timeKey: 0 for timeKey in transfer_time_type} for key in generateKeys("original")},
                "compressed": {key:{timeKey: 0 for timeKey in transfer_time_type} for key in generateKeys("compressed")}
            }
            
            for image_type in transfer_image_type:
                keys = v_data["transfer"][image_type]
                for key in keys:
                    for timeKey in transfer_time_type:
                        median_data["transfer"][image_type][key][timeKey] = get_median(v_data["transfer"][image_type][key][timeKey])
        else:
            median_data[part] = {key: 0 for key in generateKeys("compressed")}
            keys = median_data[part]
            for key in keys:
                median_data[part][key] = get_median(v_data[part][key])
    return median_data 


data = load_data()
save_data_as_json(data, "/home/rouf-linux/edge-computing/image_transfer/report_generation/raw_results/data.json")
v_data = rearrange_data_vertically(data)
save_data_as_json(v_data, "/home/rouf-linux/edge-computing/image_transfer/report_generation/raw_results/v_data.json")
avg_data = calculate_average(v_data)
save_data_as_json(avg_data, "/home/rouf-linux/edge-computing/image_transfer/report_generation/raw_results/avg_data.json")
median_data = calculate_median(v_data)
save_data_as_json(median_data, "/home/rouf-linux/edge-computing/image_transfer/report_generation/raw_results/median_data.json")

        

