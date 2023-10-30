import csv
import os
import json
json_data_base_path = '/home/rouf-linux/edge-computing/models/metrics_gen/result/2023_10_26___06_45_03'
csv_result_base_path = "/home/rouf-linux/edge-computing/models/metrics_gen/csv_result/median_result"
cameras = {
    'cam1': 'p3245_axis_20231010_020941',
    'cam2': 'p3265_axis_20231009_223413',
    'cam3': 'p3364_axis_20231009_214248',
    'cam4': 'vivotek_20231009_201139'
}
resolutions = {
    'p3245_axis_20231010_020941': ['160x90', '160x100', '160x120', '240x180', '320x180', '320x200', '320x240', '480x270', '480x300', '480x360', '640x360', '640x400', '640x480', '800x450', '800x500', '800x600', '1024x576', '1024x640', '1024x768', '1280x720', '1280x800', '1280x960', '1440x900', '1440x1080', '1920x1080'],
    'p3265_axis_20231009_223413': ['160x90', '160x100', '160x120', '240x180', '320x180', '320x200', '320x240', '480x270', '480x300', '480x360', '640x360', '640x400', '640x480', '800x450', '800x500', '800x600', '1024x576', '1024x640', '1024x768', '1280x720', '1280x800', '1280x960', '1440x900', '1440x1080', '1920x1080'], 
    'p3364_axis_20231009_214248': ['176x144', '160x90', '160x120', '240x180', '320x180', '320x240', '480x270', '480x360', '640x360', '800x450', '800x600', '640x480', '1024x640', '1280x800', '1024x768', '1280x720', '1280x960'],
    'vivotek_20231009_201139': [
        'streamid_1/quality_1', 'streamid_1/quality_2', 'streamid_1/quality_3', 'streamid_1/quality_4', 'streamid_1/quality_5', 
        'streamid_0/quality_1', 'streamid_0/quality_2', 'streamid_0/quality_3', 'streamid_0/quality_4', 'streamid_0/quality_5',
    ]
}
frames = [1, 2, 4, 8, 16, 32]
models = ["yolov5", "ssd", "retinanet"]
stat_metrics = ["mean", "median"]
metrics = ["TP", "FP", "FN", "accuracy", "recall"]

def load_all_json_data():
    json_data = []
    for i in range(10):
        exp_no = i + 1
        exp_json_path = json_data_base_path + "/" + "exp_" + str(exp_no) + ".json"
        with open(exp_json_path, 'r') as json_file:
            exp_json = json.load(json_file)
        json_data.append(exp_json)
    return json_data
def find_median(numbers):
    numbers.sort()
    n = len(numbers)
    if n % 2 == 1:
        median = numbers[n // 2]
    else:
        middle1 = numbers[n // 2 - 1]
        middle2 = numbers[n // 2]
        median = (middle1 + middle2) / 2
    return median


def calculate_median_on_all_json(json_data):
    total_exp = len(json_data)
    median = {}
    for camera in cameras:
        resolution_median = {}
        for resolution in resolutions[cameras[camera]]:
            frame_median = {}
            for frame in frames:
                key = "/" + cameras[camera] + "/" + resolution + "/" + str(frame)+ "/"
                print(key)
                key_datas = {
                    "yolov5": {
                        "mean": {
                            "TP": [],
                            "FP": [],
                            "FN": [],
                            "accuracy": [],
                            "recall": []
                        },
                        "median": {
                            "TP": [],
                            "FP": [],
                            "FN": [],
                            "accuracy": [],
                            "recall": []
                        }
                    },
                    "ssd": {
                        "mean": {
                            "TP": [],
                            "FP": [],
                            "FN": [],
                            "accuracy": [],
                            "recall": []
                        },
                        "median": {
                            "TP": [],
                            "FP": [],
                            "FN": [],
                            "accuracy": [],
                            "recall": []
                        }
                    },
                    "retinanet": {
                        "mean": {
                            "TP": [],
                            "FP": [],
                            "FN": [],
                            "accuracy": [],
                            "recall": []
                        },
                        "median": {
                            "TP": [],
                            "FP": [],
                            "FN": [],
                            "accuracy": [],
                            "recall": []
                        }
                    }
                }
                
                for i in range(total_exp):
                    key_data = json_data[i][key]
                    for model in models:
                        for metric in metrics:
                            key_datas[model][stat_metrics[1]][metric].append(key_data[model][stat_metrics[1]][metric])

                for model in models:
                    for metric in metrics:
                        key_datas[model][stat_metrics[1]][metric] = find_median(key_datas[model][stat_metrics[1]][metric])
                
                median_key_data = key_datas
                frame_median[frame] = median_key_data
            resolution_median[resolution] = frame_median
        median[camera] = resolution_median
    return median 


def generate_frame_varied_csv(median):
    for camera in cameras:
        for metric in metrics:
            table = [[metric + "- frame/model", "yolov5", "ssd", "retinanet"]]
            for frame in frames:
                median_datas = {
                    "yolov5": [],
                    "ssd": [],
                    "retinanet": []
                }
                for resolution in resolutions[cameras[camera]]:
                    for model in models:
                        median_datas[model].append(median[camera][resolution][frame][model][stat_metrics[1]][metric])
                row = [frame]
                for model in models:
                    median_datas[model] = find_median(median_datas[model])
                    row.append(round(median_datas[model], 3))
                table.append(row)
            os.makedirs(csv_result_base_path + "/frame_based/" + camera, exist_ok=True)
            with open(csv_result_base_path + "/frame_based/" + camera + "/" + metric + ".csv", 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(table)

def generate_resolution_varied_csv(median):
    for camera in cameras:
        for metric in metrics:
            table = [[metric + "- resolution/model", "yolov5", "ssd", "retinanet"]]
            for resolution in resolutions[cameras[camera]]:
                median_datas = {
                    "yolov5": [],
                    "ssd": [],
                    "retinanet": []
                }
                for frame in frames:
                    for model in models:
                        median_datas[model].append(median[camera][resolution][frame][model][stat_metrics[1]][metric])
                row = [resolution]
                for model in models:
                    median_datas[model] = find_median(median_datas[model])
                    row.append(round(median_datas[model], 3))
                table.append(row)
            os.makedirs(csv_result_base_path + "/resolution_based/" + camera, exist_ok=True)
            with open(csv_result_base_path + "/resolution_based/" + camera + "/" + metric + ".csv", 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(table)
            
                
                



json_data = load_all_json_data()
median = calculate_median_on_all_json(json_data)
generate_frame_varied_csv(median)
generate_resolution_varied_csv(median)

