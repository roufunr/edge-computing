import numpy as np
import cv2
import torch
import torchvision
from imageai.Detection import ObjectDetection
import json
import time
import os
from datetime import datetime
import sys
import logging

logging.basicConfig(filename='object_detection_calculate_metrics.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


home_directory = "/home/ubuntu/"

images_base_path = home_directory + "coco128/images/train2017"
labels_base_path = home_directory + "coco128/labels"
result_base_path = home_directory + "/edge-computing/ssd_accuracy_measure/results"
total_experiment = 11
# models = ["yolov5", "ssd", "retinanet"]
models = ["ssd"]
scaling_factors = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
interpolation_methods = {
    'INTER_NEAREST': cv2.INTER_NEAREST,
    'INTER_LINEAR': cv2.INTER_LINEAR,
    'INTER_CUBIC': cv2.INTER_CUBIC,
    'INTER_AREA': cv2.INTER_AREA,
    'INTER_LANCZOS4': cv2.INTER_LANCZOS4
}

retinanet_detector = ObjectDetection()
# detector.useCPU()
# retinanet_detector.setModelTypeAsRetinaNet()
# retinanet_detector.setModelPath(home_directory + "retinanet_model.pth")  # Specify the path to the RetinaNet model
# retinanet_detector.loadModel()

retinent_model = retinanet_detector
ssd_model = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_ssd')
ssd_utils = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_ssd_processing_utils')
ssd_model.to('cuda')
ssd_model.eval()
classes_to_labels = ssd_utils.get_coco_object_dictionary()
yolov5_model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
yolov5_model = yolov5_model.cuda()

def get_retinanet_object_list(image_path):
    detections = retinent_model.detectObjectsFromImage(input_image= image_path)
    objects = []
    for detection in detections:
        objects.append(detection["name"])
    return objects

def get_ssd_object_list(image_path):
    input = [ssd_utils.prepare_input(image_path)]
    tensor = ssd_utils.prepare_tensor(input)
    with torch.no_grad():
        detections_batch = ssd_model(tensor)
    results_per_input = ssd_utils.decode_results(detections_batch)
    best_results_per_input = [ssd_utils.pick_best(results, 0.00) for results in results_per_input]
    objects_list = []
    for image in best_results_per_input:
        object_list = []
        bboxes, classes, confidences = image
        for idx in range(len(bboxes)):
            object_list.append(classes_to_labels[classes[idx] - 1])
        objects_list.append(object_list)
    return objects_list[0]

def get_yolov5_object_list(image_path):
    objects_list = []
    cv2_images = []
    
    im = cv2.imread(image_path)[..., ::-1]
    cv2_images.append(im)  
    
    results = yolov5_model(cv2_images, size=640) # batch of images
    for idx in range(len(cv2_images)):
        objects_list.append(results.pandas().xyxy[idx]['name'].tolist())
    return objects_list[0]

def get_object_list(images_path, model):
    if model == "yolov5":
        return get_yolov5_object_list(images_path)
    elif model == "ssd": 
        return get_ssd_object_list(images_path)
    else:
        return get_retinanet_object_list(images_path)

def calculate_metrics(detected_objects, labeled_objects):
    # detected_objects = ['person', 'chair', 'keyboard', 'person']
    # labeled_objects = ['person', 'train', 'keyboard', 'mouse'
    TP = 0
    FP = 0
    FN = 0

    # Calculate TP, FP, and FN for each class
    for obj in set(detected_objects + labeled_objects):
        detected_count = detected_objects.count(obj)
        labeled_count = labeled_objects.count(obj)
        
        TP += min(detected_count, labeled_count)
        FP += max(0, detected_count - labeled_count)
        FN += max(0, labeled_count - detected_count)

    # Calculate accuracy, recall, and precision, handling the case where labeled_objects is empty
    if TP + FP == 0:
        accuracy = 0
    else:
        accuracy = TP / (TP + FP)

    if TP + FN == 0:
        recall = 0
    else:
        recall = TP / (TP + FN)

    metrics = {
        "TP": TP,
        "FP": FP,
        "FN": FN,
        "accuracy": accuracy,
        "recall": recall,
    }
    return metrics

def calculate_average_and_median(metrics_list):
    sum_metrics = {
        "TP": 0,
        "FP": 0,
        "FN": 0,
        "accuracy": 0,
        "recall": 0,
    }

    tp_values = []
    fp_values = []
    fn_values = []
    accuracy_values = []
    recall_values = []

    for metrics in metrics_list:
        for key in sum_metrics.keys():
            sum_metrics[key] += metrics[key]
            if key == "TP":
                tp_values.append(metrics[key])
            elif key == "FP":
                fp_values.append(metrics[key])
            elif key == "FN":
                fn_values.append(metrics[key])
            elif key == "accuracy":
                accuracy_values.append(metrics[key])
            elif key == "recall":
                recall_values.append(metrics[key])

    # Calculate averages
    num_tasks = len(metrics_list)
    average_metrics = {key: value / num_tasks for key, value in sum_metrics.items()}

    # Calculate medians
    median_metrics = {
        "TP": np.median(tp_values),
        "FP": np.median(fp_values),
        "FN": np.median(fn_values),
        "accuracy": np.median(accuracy_values),
        "recall": np.median(recall_values)
    }

    return average_metrics, median_metrics

def seconds_to_hms(seconds):
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return hours, minutes, seconds

def get_all_images():
    file_names = [f for f in os.listdir(images_base_path) if os.path.isfile(os.path.join(images_base_path, f))]
    image_names = [filename.split(".")[0] for filename in file_names]
    return image_names

def get_all_labels():
    file_names = [f for f in os.listdir(labels_base_path) if os.path.isfile(os.path.join(labels_base_path, f))]
    labels_names = [filename.split(".")[0] for filename in file_names]
    return labels_names

def parse_label_file(filename): 
    file_path = labels_base_path + "/" + filename
    data_list = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) == 5:
                data_dict = {
                    'idx': int(parts[0]),
                    'name': classes_to_labels[int(parts[0])],
                    'x_min': float(parts[1]),
                    'y_min': float(parts[2]),
                    'x_max': float(parts[3]),
                    'y_max': float(parts[4])
                }
                data_list.append(data_dict)
    return data_list

def get_labeled_data():
    images_list = get_all_images()
    labeled_data = {}
    for image in images_list:
        image_name = image.split(".")[0]
        image_label = parse_label_file(image_name + ".txt")
        labeled_data[image_name] = image_label
    return labeled_data

def save_label_as_json(data):
    with open(labels_base_path + "/labels.json", 'w') as json_file:
        json.dump(data, json_file, indent=4)

def save_data_as_json(data, json_path):
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def load_labeled_data():
    labels_path = "/home/ubuntu/edge-computing/ssd_accuracy_measure/more_accurate_labels.json"
    with open(labels_path, 'r') as json_file:
        labeled_data = json.load(json_file)
    return labeled_data


def downscale(image_path, scaling_factor, scaling_method): 
    image = cv2.imread(image_path)
    start_time = time.time() * 1000
    downscaled_image = cv2.resize(image, None, fx=scaling_factor, fy=scaling_factor, interpolation=interpolation_methods[scaling_method])
    end_time = time.time() * 1000
    elapsed_time = end_time - start_time
    return downscaled_image

def upscale(downscaled_image, scaling_factor, scaling_method): 
    start_time = time.time() * 1000
    upscaled_image = cv2.resize(downscaled_image, None, fx=1/scaling_factor, fy=1/scaling_factor, interpolation=interpolation_methods[scaling_method])
    end_time = time.time() * 1000
    elapsed_time = end_time - start_time
    return upscaled_image

def save_processed_image(cv2_image):
    os.makedirs("tmp", exist_ok=True)
    tmp_image_path = "./" + "tmp/" + str(int(time.time() * 1000)) + ".jpg"
    cv2.imwrite(tmp_image_path, cv2_image)
    return tmp_image_path

def get_labeled_objects(labeled_image):
    labeled_objects = []
    for object in labeled_image:
        labeled_objects.append(object["name"])
    return labeled_objects

def get_inferred_objects(image_path):
    inferred_objects = {
        "yolov5": get_yolov5_object_list(image_path),
        "ssd": get_ssd_object_list(image_path),
        "retinanet": get_retinanet_object_list(image_path)
    }
    return inferred_objects

def get_inferred_image_metrics(labeled_objects, inferred_objects):
    inferred_metrics = {}
    for model in models:
        inferred_metrics[model] = calculate_metrics(inferred_objects[model], labeled_objects)
    return inferred_metrics

def run_experiment(labeled_data, exp_id):
    logging.info(str(exp_id) + " :::: " + " STARTED!")
    exp = {}
    total_data = len(labeled_data)
    completed_data = 0
    for image_id in labeled_data:
        start_time = time.time()
        metric = {}
        labeled_objects = labeled_data[image_id]
        
        original_image_path = "/home/ubuntu/coco2017/val2017/" + image_id + ".jpg"
        oi_inferred_objects = get_ssd_object_list(original_image_path)
        metric["original"] = calculate_metrics(oi_inferred_objects, labeled_objects)

        metric["scaled"] = {}
        for scaling_factor in scaling_factors:
            interpolation_method_metric = {}
            for ip_method in interpolation_methods:
                downscaled_image = downscale(original_image_path, scaling_factor=scaling_factor, scaling_method=ip_method)
                upscaled_image = upscale(downscaled_image, scaling_factor=scaling_factor, scaling_method=ip_method)
                processed_image_path = save_processed_image(upscaled_image)
                pi_inferred_objects = get_ssd_object_list(processed_image_path)
                os.remove(processed_image_path)
                interpolation_method_metric[ip_method] = calculate_metrics(labeled_objects, pi_inferred_objects)
            metric["scaled"][str(scaling_factor)] = interpolation_method_metric
        exp[image_id] = metric
        completed_data += 1
        progress = round((completed_data / total_data) * 100, 2)
        end_time = time.time()
        h,m,s = seconds_to_hms(round(end_time - start_time))
        logging.info(str(exp_id) + " :::: " + " PROGRESS ==> " + str(progress) + "%" + " " + "ELAPSED_TIME ==> " + str(h) + ":" + str(m) + ":" + str(s))
    logging.info(str(exp_id) + " :::: " + " DONE!")
    return exp


labeled_data = load_labeled_data()
for i in range(total_experiment):
    exp_data = run_experiment(labeled_data, i)
    save_data_as_json(exp_data, result_base_path + "/" + "exp_" + str(i) + ".json")
