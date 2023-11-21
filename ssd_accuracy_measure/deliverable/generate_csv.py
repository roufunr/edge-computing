import json
import os
import csv

image_types = ["original", "scaled"]
models = ["yolov5", "ssd", "retinanet"]
metrics = ["TP", "FP", "FN", "accuracy", "recall"]
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
        data = json.load(json_file)
    return data

def write_2d_list_to_csv(csv_path, data):
    try:
        with open(csv_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            for row in data:
                csv_writer.writerow(row)
        print(f"CSV file saved to {csv_path}")
    except Exception as e:
        print(f"Error: {e}")


avg_data = load_json("/Users/abdurrouf/edge-computing/ssd_accuracy_measure/results/avg.json")

rows = []
header = []
for ip_method in ip_methods:
    # heaader row
    header.append(ip_methods_name_mapper[ip_method])
rows.append(header)

# append scaling row
for scaling_factor in scaling_factors:
    row = [scaling_factor]
    for ip_method in ip_methods:
        row.append(avg_data[image_types[1]][str(scaling_factor)][ip_method]["accuracy"])
    rows.append(row)

# original accuracy row
original_row = ["original", avg_data["original"]["accuracy"], avg_data["original"]["accuracy"], avg_data["original"]["accuracy"], avg_data["original"]["accuracy"], avg_data["original"]["accuracy"]]
rows.append(original_row)

csv_base_path = "/Users/abdurrouf/edge-computing/ssd_accuracy_measure/results/ssd_accuracy.csv"
write_2d_list_to_csv(csv_base_path, rows) 