import json
import os 
import sys

json_base_path = "/home/rouf-linux/models/json_parser/data/"
result_base_path = "/home/rouf-linux/models/json_parser/result/"

procedures = ['detection', 'transfer']
instances = [['orin', 'cloud_virginia'], ['orin', 'cloud_virginia', 'cloud_california']]
models = ["yolov5", "ssd", "retinanet"]
devices = ["cuda", "cpu"]
transfer_metrices = ["transfer_time", "disk_write_time", "response_time"]

def load_json(json_path):
    json_data = {}
    with open(json_path, "r") as json_file:
        json_data = json.load(json_file)
    return json_data

def load_directory(folder_path): 
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    data = [0] * len(json_files)
    for json_file in json_files:
        exp_idx = json_file.split("_")[1]
        file_path = os.path.join(folder_path, json_file)
        with open(file_path, 'r') as f:
            json_data = json.load(f)
            data[int(exp_idx) - 1] = json_data
    return data

def load_part_of_experiment(base_path):
    raw_data = {
        'detection': {
            'orin': load_directory(base_path + "/detection/orin"),
            'cloud_virginia': load_directory(base_path + "/detection/cloud_virginia")
        },
        'transfer': {
            'orin': load_directory(base_path + "/transfer/orin"),
            'cloud_virginia': load_directory(base_path + "/transfer/cloud_virginia"), 
            'cloud_california': load_directory(base_path + "/transfer/cloud_california"), 
        }
    }
    
    number_of_exp = len(raw_data['detection']['orin'])
    data = []
    for i in range(number_of_exp):
        exp = {
            'detection': {
                'orin': raw_data['detection']['orin'][i],
                'cloud_virginia': raw_data['detection']['cloud_virginia'][i]
            },
            'transfer': {
                'orin': raw_data['transfer']['orin'][i],
                'cloud_virginia': raw_data['transfer']['cloud_virginia'][i], 
                'cloud_california': raw_data['transfer']['cloud_california'][i] 
            }
        }
        data.append(exp)
    return data

def calculate_average(data): 
    total_exp = len(data)
    keys = list(data[0]['detection']['orin'].keys())
    avg_data = {
        'detection': {
            'orin': {},
            'cloud_virginia': {}
        }, 
        'transfer': {
            'orin': {},
            'cloud_virginia': {},
            'cloud_california': {}
        }
    }

    for key in keys:
        for procedure in range(len(procedures)):
            for instance in range(len(instances[procedure])):
                key_avg = {}
                if procedures[procedure] == "detection": 
                    model_avg = {}
                    for model in range(len(models)):
                        device_avg = {}
                        for device in range(len(devices)):
                            sum = 0
                            for i in range(total_exp): 
                                sum += data[i][procedures[procedure]][instances[procedure][instance]][key][models[model]][devices[device]]
                            avg = sum/total_exp
                            device_avg[devices[device]] = avg
                        model_avg[models[model]] = device_avg
                    key_avg = model_avg
                        
                else:
                    transfer_metric_avg = {}
                    for transfer_metric in transfer_metrices:
                        sum = 0
                        for i in range(total_exp): 
                            sum += data[i][procedures[procedure]][instances[procedure][instance]][key][transfer_metric]
                        avg = sum/total_exp
                        transfer_metric_avg[transfer_metric] = avg
                    key_avg = transfer_metric_avg
                avg_data[procedures[procedure]][instances[procedure][instance]][key] = key_avg
    return avg_data

def get_camera_details(avg):
    keys = list(data[0]['detection']['orin'].keys())
    details = {}
    for key in keys:
        pieces = key.split("/")
        camera_name = pieces[1]
        frame_count = pieces[len(pieces) - 2]
        image_type = ((key.replace("/" + camera_name + "/", "")).replace("/" + frame_count + "/", ""))
        if camera_name not in details:
            details[camera_name] = {}
        if image_type not in details[camera_name]: 
            details[camera_name][image_type] = {}
        if frame_count not in details[camera_name][image_type]: 
            details[camera_name][image_type][frame_count] = 0
    
    return details

def generate_result_csv_dirs(camera_details, csv_base_path):
    cameras_list = list(camera_details)
    for camera_name in cameras_list:
        for procedure in procedures:
            if procedure == "detection":
                for model in models:
                    os.makedirs(csv_base_path + "/" + camera_name + "/" + procedure + "/" + model)
            else:
                os.makedirs(csv_base_path + "/" + camera_name + "/" + procedure )



# def generate_detection_csv():

# def generate_tranfer_csv():


# def generate_csv(camera_details, csv_base_path, data):
#     # generate detection csv
#     generate_detection_csv(camera_details, csv_base_path, data)
#     # generate transfer csv
#     generate_tranfer_csv(camera_details, csv_base_path, data)


data = load_part_of_experiment(json_base_path)
avg = calculate_average(data)
camera_data_hierarchy = get_camera_details(avg)
generate_result_csv_dirs(camera_data_hierarchy, result_base_path)




