import os
import pandas
import csv
import json

source_data_path = "/home/rouf-linux/edge-computing/transfer_detection_sum/result/"
result_path = "/home/rouf-linux/edge-computing/transfer_detection_sum/deliverables/"
cameras = ["cam1", "cam2", "cam3", "cam4"]
procedures = ["transfer", "detection"]
instances = ["cloud_virginia",  "cloud_california", "orin"]
transfer_metric = "response_time"
models = ["yolov5", "ssd", "retinanet"]
devices = ["cuda", "cpu"]

def generate_concat_csv(csv_files, camera, device):
    concatenated_data = pandas.DataFrame()
    for i, file in enumerate(csv_files):
        data = pandas.read_csv(file)
        if i < len(csv_files) - 1:
            data['Empty_Column'] = ''
        concatenated_data = pandas.concat([concatenated_data, data], axis=1)
    concatenated_data.to_csv(result_path + camera + "_" + device + '.csv', index=False)

for camera in cameras:
    for device in devices:
        csv_filenames = []
        for model in models:
            for instance in instances:
                csv_file_path = source_data_path + camera + "/" + instance + "/" + model + "/" + device + ".csv"
                csv_filenames.append(csv_file_path)
                #print(csv_file_path)
        print("processing..", camera, device)
        generate_concat_csv(csv_filenames, camera, device)