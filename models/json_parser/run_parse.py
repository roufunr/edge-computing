import json
import os 
import sys
import csv

exp_no = "median"
exp = "exp_" + str(exp_no)
json_base_path = "/home/rouf-linux/edge-computing/models/json_parser/data/"
result_base_path = "/home/rouf-linux/edge-computing/models/json_parser/result/" + exp + "/"
# os.makedirs(result_base_path)

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

def getMedian(data):
    data.sort()
    n = len(data)
    if n % 2 == 1:
        median = data[n // 2]
    else:
        # If the number of elements is even, the median is the average of the two middle elements
        middle1 = data[n // 2 - 1]
        middle2 = data[n // 2]
        median = (middle1 + middle2) / 2
    return median
def calculate_median(data): 
    total_exp = len(data)
    keys = list(data[0]['detection']['orin'].keys())
    median_data = {
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
                key_median = {}
                if procedures[procedure] == "detection": 
                    model_median = {}
                    for model in range(len(models)):
                        device_median = {}
                        for device in range(len(devices)):
                            data_arr = []
                            for i in range(total_exp): 
                                data_arr.append(data[i][procedures[procedure]][instances[procedure][instance]][key][models[model]][devices[device]])
                            device_median[devices[device]] = getMedian(data_arr)
                        model_median[models[model]] = device_median
                    key_median = model_median
                        
                else:
                    transfer_metric_median= {}
                    for transfer_metric in transfer_metrices:
                        data_arr = []
                        for i in range(total_exp): 
                            data_arr.append(data[i][procedures[procedure]][instances[procedure][instance]][key][transfer_metric])
                        transfer_metric_median[transfer_metric] = getMedian(data_arr)
                    key_median = transfer_metric_median
                median_data[procedures[procedure]][instances[procedure][instance]][key] = key_median
    return median_data


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
        for procedure in range(len(procedures)):
            for instance in range(len(instances[procedure])):
                if procedures[procedure] == "detection":
                    for model in models:
                        os.makedirs(csv_base_path + "/" + camera_name + "/" + procedures[procedure]  +"/" + instances[procedure][instance] + "/" + model, exist_ok=True)
                else: 
                    os.makedirs(csv_base_path + "/" + camera_name + "/" + procedures[procedure] + "/" + instances[procedure][instance], exist_ok= True)

def generate_csv(csv_base_path, 
                 data, 
                 camera_name, 
                 specific_camera_details, 
                 procedure, 
                 instance, 
                 model=None, 
                 device=None, 
                 transfer_metric=None):
    csv_path = csv_base_path + camera_name + "/" + procedure + "/" + instance
    if procedure == "detection": 
        csv_path += "/" + model + "/" + device + ".csv"
    else: 
        csv_path += "/" + transfer_metric + ".csv"
    
    column_names = ["size", "image_quality", "1", "2", "4", "8", "16", "32"]
    vivotek_image_quality_mapper = {
        "streamid_0": {
            "quality_1": "70kb",
            "quality_2": "83kb",
            "quality_3": "120kb",
            "quality_4": "168kb",
            "quality_5": "218kb",
        },
        "streamid_1": {
            "quality_1": "11kb",
            "quality_2": "13kb",
            "quality_3": "19kb",
            "quality_4": "25kb",
            "quality_5": "31kb",
        }
    }
    image_details = {}
    for image_quality in specific_camera_details:
        if "x" in image_quality:
            pieces = image_quality.split("x")
            size = int(pieces[0]) * int(pieces[1])
            image_details[image_quality] = size
        else: 
            pieces = image_quality.split("/")
            image_new_quality = vivotek_image_quality_mapper[pieces[0]][pieces[1]]
            size = int(image_new_quality.replace("kb", ""))
            image_details[image_quality] = size
    
    sorted_image_details = dict(sorted(image_details.items(), key=lambda item: item[1]))
    
    rows = []
    rows.append(column_names)
    for image_detail in sorted_image_details:
        row = []
        row.append(image_details[image_detail])
        if "/" in image_detail:
            pieces = image_detail.split("/")
            image_quality = vivotek_image_quality_mapper[pieces[0]][pieces[1]]
            row.append(image_quality)
        else: 
            row.append(image_detail)
        
        for i in range(6):
            key = "/" + camera_name + "/" + image_detail + "/" + str(2**i) + "/"
            print(procedure, instance, "searching: " , key)
            if transfer_metric == None:
                
                elapsed_time = round(data[procedure][instance][key][model][device])
            else: 
                elapsed_time = round(data[procedure][instance][key][transfer_metric])
            row.append(elapsed_time)
        rows.append(row)

    with open(csv_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write each row to the CSV file
        for row in rows:
            csv_writer.writerow(row)
    print(f'CSV file "{csv_path}" has been created successfully.')
        

def generate_all_csv(csv_base_path, data, camera_details): 
    camera_names = list(camera_details)
    for camera_name in camera_names:
        specific_camera_details = camera_details[camera_name]
        for procedure in range(len(procedures)):
            for instance in range(len(instances[procedure])):
                if procedures[procedure] == "detection":
                    for model in models:
                        for device in devices:
                            generate_csv(csv_base_path, 
                                        data, 
                                        camera_name, 
                                        specific_camera_details, 
                                        procedures[procedure], 
                                        instances[procedure][instance], 
                                        model=model, 
                                        device=device, 
                                        transfer_metric=None)
                else: 
                    for transfer_metric in transfer_metrices:
                        generate_csv(csv_base_path, 
                                        data, 
                                        camera_name, 
                                        specific_camera_details, 
                                        procedures[procedure], 
                                        instances[procedure][instance], 
                                        model=None, 
                                        device=None, 
                                        transfer_metric=transfer_metric)


data = load_part_of_experiment(json_base_path)
avg = calculate_average(data)
median = calculate_median(data)
camera_data_hierarchy = get_camera_details(median)
generate_result_csv_dirs(camera_data_hierarchy, result_base_path)
generate_all_csv(result_base_path, median, camera_data_hierarchy)




