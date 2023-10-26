import cv2
import torch
import torchvision
from torchvision.models.detection import retinanet_resnet50_fpn, RetinaNet_ResNet50_FPN_Weights
import json
import time
import os
from datetime import datetime

retinanet_coco_class_mapper = {
    0: 'person',
    1: 'bicycle',
    2: 'car',
    3: 'motorcycle',
    4: 'airplane',
    5: 'bus',
    6: 'train',
    7: 'truck',
    8: 'boat',
    9: 'traffic light',
    10: 'fire hydrant',
    11: 'stop sign',
    12: 'parking meter',
    13: 'bench',
    14: 'bird',
    15: 'cat',
    16: 'dog',
    17: 'horse',
    18: 'sheep',
    19: 'cow',
    20: 'elephant',
    21: 'bear',
    22: 'zebra',
    23: 'giraffe',
    24: 'backpack',
    25: 'umbrella',
    26: 'handbag',
    27: 'tie',
    28: 'suitcase',
    29: 'frisbee',
    30: 'skis',
    31: 'snowboard',
    32: 'sports ball',
    33: 'kite',
    34: 'baseball bat',
    35: 'baseball glove',
    36: 'skateboard',
    37: 'surfboard',
    38: 'tennis racket',
    39: 'bottle',
    40: 'wine glass',
    41: 'cup',
    42: 'fork',
    43: 'knife',
    44: 'spoon',
    45: 'bowl',
    46: 'banana',
    47: 'apple',
    48: 'sandwich',
    49: 'orange',
    50: 'broccoli',
    51: 'carrot',
    52: 'hot dog',
    53: 'pizza',
    54: 'donut',
    55: 'cake',
    56: 'chair',
    57: 'couch',
    58: 'potted plant',
    59: 'bed',
    60: 'dining table',
    61: 'toilet',
    62: 'TV',
    63: 'laptop',
    64: 'mouse',
    65: 'remote',
    66: 'keyboard',
    67: 'cell phone',
    68: 'microwave',
    69: 'oven',
    70: 'toaster',
    71: 'sink',
    72: 'refrigerator',
    73: 'book',
    74: 'clock',
    75: 'vase',
    76: 'scissors',
    77: 'teddy bear',
    78: 'hair drier',
    79: 'toothbrush',
    80: 'hair brush',
    81: 'comb',
    82: 'toothpaste',
    83: 'soap',
    84: 'washing machine',
    85: 'microwave oven',
    86: 'refrigerator',
    87: 'oven',
    88: 'cabinet',
    89: 'stove',
    90: 'toaster'
}

source_dataset_base_path = "/home/ubuntu/edge-computing/models/test_data"
result_base_path = "/home/ubuntu/edge-computing/models/accuracy_exp/result"
total_experiment = 11
models = ["yolov5", "ssd", "retinanet"]

retinent_model = retinanet_resnet50_fpn(weights=RetinaNet_ResNet50_FPN_Weights.DEFAULT)
retinent_model = retinent_model.to("cuda")
retinent_model.eval()

ssd_model = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_ssd')
ssd_utils = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_ssd_processing_utils')
ssd_model.to('cuda')
ssd_model.eval()

yolov5_model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
yolov5_model = yolov5_model.cuda()

def get_retinanet_object_list(images_path):
    objects_list = []
    for image_path in images_path:
        object_list = []
        image = cv2.imread(image_path)
        transform = torchvision.transforms.Compose([torchvision.transforms.ToTensor(), torchvision.transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.299, 0.224, 0.225])])
        input_image = transform(image)
        input_image=input_image.unsqueeze(0)
        input_image=input_image.to("cuda:0")
        with torch.no_grad():
            prediction = retinent_model(input_image)
        labels = prediction[0]['labels']
        for label in labels: 
            label_idx = int(label.item()) - 1
            object_list.append(retinanet_coco_class_mapper[label_idx])
        objects_list.append(object_list)
    return objects_list

def get_ssd_object_list(images_path):
    inputs = [ssd_utils.prepare_input(uri) for uri in images_path]
    tensor = ssd_utils.prepare_tensor(inputs)
    with torch.no_grad():
        detections_batch = ssd_model(tensor)
    results_per_input = ssd_utils.decode_results(detections_batch)
    best_results_per_input = [ssd_utils.pick_best(results, 0.00) for results in results_per_input]
    classes_to_labels = ssd_utils.get_coco_object_dictionary()
    
    objects_list = []
    for image in best_results_per_input:
        object_list = []
        bboxes, classes, confidences = image
        for idx in range(len(bboxes)):
            object_list.append(classes_to_labels[classes[idx] - 1])
        objects_list.append(object_list)
    return objects_list

def get_yolov5_object_list(images_path):
    objects_list = []
    cv2_images = []
    for image_path in images_path:
        im = cv2.imread(image_path)[..., ::-1]
        cv2_images.append(im)  
    
    results = yolov5_model(cv2_images, size=640) # batch of images
    for idx in range(len(images_path)):
        objects_list.append(results.pandas().xyxy[idx]['name'].tolist())
    return objects_list

def get_object_list(images_path, model):
    if model == "yolov5":
        return get_yolov5_object_list(images_path)
    elif model == "ssd": 
        return get_ssd_object_list(images_path)
    else:
        return get_retinanet_object_list(images_path)

with open(source_dataset_base_path + '/labels.json', 'r') as json_file:
    labels = json.load(json_file)
total_data = len(labels)
path_dict = {}
label_dict = {}
for label in labels:
    path = label['image_path']
    objects = label['objects']
    objects_name = []
    for object in objects:
        objects_name.append(object['name'])
    image_name = path.split("/")[-1]
    dir_path = path.replace(image_name, "")
    if dir_path in path_dict:
        path_dict[dir_path].append(source_dataset_base_path + path)
        label_dict[dir_path].append(objects_name)
    else:
        path_dict[dir_path] = [source_dataset_base_path + path]
        label_dict[dir_path] = [objects_name]
    

   

timestamp = time.time()
parent_dir = result_base_path + "/" +  datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
os.makedirs(parent_dir, exist_ok=True)
for i in range(total_experiment): 
    exp_dir = parent_dir + "/" + "exp_" + str(i)
    os.makedirs(exp_dir)
    for model in models:
        result_dict = {}
        for key in path_dict:
            inferred_objects = get_object_list(path_dict[key], model)
            labeled_objects = label_dict[key]
            accuracies = []
            for object_list_idx in range(len(labeled_objects)):
                total_objects = len(labeled_objects[object_list_idx])
                detected_objects = 0
                for idx in range(len(labeled_objects[object_list_idx])):
                    object_name = labeled_objects[object_list_idx][idx]
                    if object_name in inferred_objects[object_list_idx]:
                        detected_objects += 1
                        inferred_objects[object_list_idx].remove(object_name)
                accuracy = detected_objects / total_objects



    