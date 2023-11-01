import os
import pandas
import csv
import json

source_data_path = "/home/rouf-linux/edge-computing/transfer_detection_sum/source_data/current_data/"
result_path = "/home/rouf-linux/edge-computing/transfer_detection_sum/before_sum/current/transfer/"
cameras = ["cam1", "cam2", "cam3", "cam4"]
procedures = ["transfer"]
instances = ["cloud_virginia", "cloud_california", "orin"]



def generate_concat_csv(csv_files, camera):
    concatenated_data = pandas.DataFrame()
    for i, file in enumerate(csv_files):
        data = pandas.read_csv(file)
        if i < len(csv_files) - 1:
            data['                               '] = ''
        concatenated_data = pandas.concat([concatenated_data, data], axis=1)
    concatenated_data.to_csv(result_path + camera + '_transfer_time.csv', index=False)

for camera in cameras:
    csv_files = []
    for instance in instances:
        csv_file_path = source_data_path + camera + "/" + procedures[0] + "/" + instance + "/" + "response_time.csv"
        csv_files.append(csv_file_path)
    generate_concat_csv(csv_files, camera)