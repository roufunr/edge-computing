import os
import pandas
import csv
import json

source_data_path = "/home/rouf-linux/edge-computing/transfer_detection_sum/source_data/current_data/"
result_path = "/home/rouf-linux/edge-computing/transfer_detection_sum/result/current_result/"
cameras = ["cam1", "cam2", "cam3", "cam4"]
procedures = ["transfer", "detection"]
instances = ["orin", "cloud_virginia"]
transfer_metric = "response_time"
models = ["yolov5", "ssd", "retinanet"]
devices = ["cuda", "cpu"]

for camera in cameras:
    transfer_instance = "orin"
    detection_instance = "orin"
    for model in models:
        for device in devices:
            print("processing ...", camera, transfer_instance, model, device)
            #load transfer_csv
            transfer_time_csv_path = source_data_path + camera + "/" + procedures[0] + "/" + transfer_instance + "/" + transfer_metric + ".csv"
            detection_time_csv_path = source_data_path + camera + "/" + procedures[1] + "/" + detection_instance + "/" + model + "/" + device + ".csv"
            transfer_time_df = pandas.read_csv(transfer_time_csv_path)
            detection_time_df = pandas.read_csv(detection_time_csv_path)
            common_columns = transfer_time_df.columns[:2]
            summed_data = transfer_time_df.drop(columns=common_columns) + detection_time_df.drop(columns=common_columns)
            result_df = pandas.concat([transfer_time_df[common_columns], summed_data], axis=1)

            save_dir_path = result_path + camera + "/" + transfer_instance + "/" + model + "/"
            filename = device + ".csv"

            os.makedirs(save_dir_path, exist_ok=True)
            result_df.to_csv(save_dir_path + filename, index=False)


                
                