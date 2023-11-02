import json
import os

image_types = ["original", "scaled"]
models = ["yolov5", "ssd", "retinanet"]
metrics = ["TP", "FP", "FN", "accuracy", "recall"]
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
def load_json(json_path):
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
    return data

def generate_empty_dict():
    empty_dict = {}
    for image_type in image_types:
        if image_type == "original":
            models_dict = {}
            for model in models:
                metrics_dict = {}
                for metric in metrics:
                    metrics_dict[metric] = 0
                models_dict[model] = metrics_dict
            empty_dict[image_type] = models_dict
        else: 
            scaling_dict = {}
            for scaling_factor in scaling_factors:
                ip_dict = {}
                for ip_method in ip_methods:
                    models_dict = {}
                    for model in models:
                        metrics_dict = {}
                        for metric in metrics:
                            metrics_dict[metric] = 0
                        models_dict[model] = metrics_dict
                    ip_dict[ip_method] = models_dict
                scaling_dict[str(scaling_factor)] = ip_dict
            empty_dict[image_type] = scaling_dict
    return empty_dict

def calculate_average(data):
    sum_dict = generate_empty_dict()
    total_data = len(data)
    for image_id in data:
        image_dict = data[image_id]
        
        for image_type in image_types:
            if image_type == "original":
                for model in models:
                    for metric in metrics:
                        sum_dict[image_type][model][metric] += image_dict[image_type][model][metric]
            else: 
                for scaling_factor in scaling_factors:
                    for ip_method in ip_methods:
                        for model in models:
                            for metric in metrics:
                                sum_dict[image_type][str(scaling_factor)][ip_method][model][metric] += image_dict[image_type][str(scaling_factor)][ip_method][model][metric]
                            
        
    for image_type in image_types:
        if image_type == "original":
            for model in models:
                for metric in metrics:
                    sum_dict[image_type][model][metric] /= total_data
        else: 
            for scaling_factor in scaling_factors:
                for ip_method in ip_methods:
                    for model in models:
                        for metric in metrics:
                            sum_dict[image_type][str(scaling_factor)][ip_method][model][metric] /= total_data

    avg_dict = sum_dict
    return avg_dict

data = load_json("/home/ubuntu/edge-computing/models/scaled_image_detection/result/exp_0.json")
avg_dict = calculate_average(data)

save_data_as_json(avg_dict, "/home/ubuntu/edge-computing/models/scaled_image_detection/result/avg.json")