import csv
import os
import json
json_data_base_path = '/Users/abdurrouf/edge-computing/models/metrics_gen/result/2023_10_26___06_45_03'
csv_result_base_path = "/Users/abdurrouf/edge-computing/models/metrics_gen/csv_result"
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
def calculate_mean_on_all_json(json_data):
    total_exp = len(json_data)
    avg = {}
    for camera in cameras:
        resolution_avg = {}
        for resolution in resolutions[cameras[camera]]:
            frame_avg = {}
            for frame in frames:
                key = "/" + cameras[camera] + "/" + resolution + "/" + str(frame)+ "/"
                print(key)
                sum_key_data = {
                    "yolov5": {
                        "mean": {
                            "TP": 0,
                            "FP": 0,
                            "FN": 0,
                            "accuracy": 0,
                            "recall": 0
                        },
                        "median": {
                            "TP": 0,
                            "FP": 0,
                            "FN": 0,
                            "accuracy": 0,
                            "recall": 0
                        }
                    },
                    "ssd": {
                        "mean": {
                            "TP": 0,
                            "FP": 0,
                            "FN": 0,
                            "accuracy": 0,
                            "recall": 0
                        },
                        "median": {
                            "TP": 0,
                            "FP": 0,
                            "FN": 0,
                            "accuracy": 0,
                            "recall": 0
                        }
                    },
                    "retinanet": {
                        "mean": {
                            "TP": 0,
                            "FP": 0,
                            "FN": 0,
                            "accuracy": 0,
                            "recall": 0
                        },
                        "median": {
                            "TP": 0,
                            "FP": 0,
                            "FN": 0,
                            "accuracy": 0,
                            "recall": 0
                        }
                    }
                }
                
                for i in range(total_exp):
                    key_data = json_data[i][key]
                    for model in models:
                        for stat_metric in stat_metrics:
                            for metric in metrics:
                                sum_key_data[model][stat_metric][metric] += key_data[model][stat_metric][metric]

                for model in models:
                    for stat_metric in stat_metrics:
                        for metric in metrics:
                            sum_key_data[model][stat_metric][metric] /= total_exp
                
                avg_key_data = sum_key_data
                frame_avg[frame] = avg_key_data
            resolution_avg[resolution] = frame_avg
        avg[camera] = resolution_avg
    return avg 
def generate_frame_varied_csv(avg):
    for camera in cameras:
        for metric in metrics:
            table = [[metric + "- frame/model", "yolov5", "ssd", "retinanet"]]
            for frame in frames:
                sum = {
                    "yolov5": 0,
                    "ssd": 0,
                    "retinanet": 0
                }
                for resolution in resolutions[cameras[camera]]:
                    for model in models:
                        sum[model] += avg[camera][resolution][frame][model][stat_metrics[0]][metric]
                row = [frame]
                for model in models:
                    sum[model] /= len(resolutions[cameras[camera]])
                    row.append(round(sum[model], 3))
                table.append(row)
            os.makedirs(csv_result_base_path + "/frame_based/" + camera, exist_ok=True)
            with open(csv_result_base_path + "/frame_based/" + camera + "/" + metric + ".csv", 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(table)

def generate_resolution_varied_csv(avg):
    for camera in cameras:
        for metric in metrics:
            table = [[metric + "- resolution/model", "yolov5", "ssd", "retinanet"]]
            for resolution in resolutions[cameras[camera]]:
                sum = {
                    "yolov5": 0,
                    "ssd": 0,
                    "retinanet": 0
                }
                for frame in frames:
                    for model in models:
                        sum[model] += avg[camera][resolution][frame][model][stat_metrics[0]][metric]
                row = [resolution]
                for model in models:
                    sum[model] /= len(frames)
                    row.append(round(sum[model], 3))
                table.append(row)
            os.makedirs(csv_result_base_path + "/resolution_based/" + camera, exist_ok=True)
            with open(csv_result_base_path + "/resolution_based/" + camera + "/" + metric + ".csv", 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(table)
            
                
                



json_data = load_all_json_data()
avg = calculate_mean_on_all_json(json_data)
generate_frame_varied_csv(avg)
generate_resolution_varied_csv(avg)

