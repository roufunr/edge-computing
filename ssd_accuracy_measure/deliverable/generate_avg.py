import os
import json

def load_from_json(json_path):
    with open(json_path, 'r') as json_file:
        # Load JSON data into a dictionary
        data = json.load(json_file)
    return data

def save_as_a_json(json_file_path, json_dict):
    with open(json_file_path, 'w') as json_file:
        json.dump(json_dict, json_file)
        
load_data = load_from_json("/Users/abdurrouf/edge-computing/ssd_accuracy_measure/results/exp_0.json")

image_types = ["original", "scaled"]
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

def generate_empty_dict():
    empty_dict = {}
    for image_type in image_types:
        if image_type == "original":
            metrics_dict = {}
            for metric in metrics:
                metrics_dict[metric] = 0
            empty_dict[image_type] = metrics_dict
        else: 
            scaling_dict = {}
            for scaling_factor in scaling_factors:
                ip_dict = {}
                for ip_method in ip_methods:
                    metrics_dict = {}
                    for metric in metrics:
                        metrics_dict[metric] = 0
                    ip_dict[ip_method] = metrics_dict
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
                for metric in metrics:
                    sum_dict[image_type][metric] += image_dict[image_type][metric]
            else: 
                for scaling_factor in scaling_factors:
                    for ip_method in ip_methods:
                        for metric in metrics:
                            sum_dict[image_type][str(scaling_factor)][ip_method][metric] += image_dict[image_type][str(scaling_factor)][ip_method][metric]
                        
        
    for image_type in image_types:
        if image_type == "original":
            for metric in metrics:
                sum_dict[image_type][metric] /= total_data
        else: 
            for scaling_factor in scaling_factors:
                for ip_method in ip_methods:
                    for metric in metrics:
                        sum_dict[image_type][str(scaling_factor)][ip_method][metric] /= total_data

    avg_dict = sum_dict
    return avg_dict

data = load_from_json("/Users/abdurrouf/edge-computing/ssd_accuracy_measure/results/exp_0.json")
avg_dict = calculate_average(data)

save_as_a_json("/Users/abdurrouf/edge-computing/ssd_accuracy_measure/results/avg.json", avg_dict)
