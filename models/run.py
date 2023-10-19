import cv2
from PIL import Image
import torch
import torchvision
import json
import os
from torchvision.models.detection import retinanet_resnet50_fpn, RetinaNet_ResNet50_FPN_Weights
from time import time
import copy
from datetime import datetime
import sys
import logging
logging.basicConfig(filename='dl.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


sys.stdout = open('nohup.out', 'a')
sys.stderr = sys.stdout


#load model
models = {}

yolov5 = [torch.hub.load('ultralytics/yolov5', 'yolov5s'), torch.hub.load('ultralytics/yolov5', 'yolov5s')]

ssd_utils = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_ssd_processing_utils')
ssd_model = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_ssd')
ssd_model_cuda = copy.deepcopy(ssd_model).to('cuda')
ssd_model_cuda.eval()
ssd_model_cpu = copy.deepcopy(ssd_model).to('cpu')
ssd_model_cpu.eval()

retinanet = [retinanet_resnet50_fpn(weights=RetinaNet_ResNet50_FPN_Weights.DEFAULT), retinanet_resnet50_fpn(weights=RetinaNet_ResNet50_FPN_Weights.DEFAULT)]
retinanet[0].to("cuda").eval()
retinanet[1].to("cpu").eval()

models = {
    'yolov5': {
        'cuda': yolov5[0].cuda(), 
        'cpu': yolov5[1].cpu()
    },
    'ssd': {
        'cuda': ssd_model_cuda, 
        'cpu': ssd_model_cpu
    },
    'retinanet': {
        'cuda': retinanet[0], 
        'cpu': retinanet[1]    
    }
}



def run_yolov5(images_path, device): 
    images = []
    for image_path in images_path:         
        image = cv2.imread(image_path)[..., ::-1]
        images.append(image)
    # Inference
    strt = time() * 1000
    results = models['yolov5'][device](images, size=640) # batch of images
    end = time() * 1000
    return end - strt


def run_ssd(images_path, device): 
    inputs = [ssd_utils.prepare_input(image) for image in images_path]
    tensor = ssd_utils.prepare_tensor(inputs).to(device)
    with torch.no_grad():
        start_time = time() * 1000
        detections_batch = models['ssd'][device](tensor)
        end_time = time() * 1000

    return end_time - start_time


def run_retinanet(images_path, device): 
    transform = torchvision.transforms.Compose([torchvision.transforms.ToTensor(), torchvision.transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.299, 0.224, 0.225])])
    total_elapsed_time = 0
    for image_path in images_path:
        image = cv2.imread(image_path)
    	#Transform and preprocess the image
        input_image = transform(image)
        input_image = input_image.unsqueeze(0)
        input_image = input_image.to(device)
        # Perform object detection
        with torch.no_grad():
            start_time = time() * 1000
            prediction = models['retinanet'][device](input_image)
            end_time = time() * 1000
        elapsed_time = end_time - start_time 
        #print('elapsed_time', elapsed_time)
        total_elapsed_time += elapsed_time
    return total_elapsed_time


def run_detection(images_path):
    result = {
        'yolov5': {
            'cuda': run_yolov5(images_path, 'cuda'), 
            'cpu': run_yolov5(images_path, 'cpu')
        },
        'ssd': {
            'cuda': run_ssd(images_path, 'cuda'), 
            'cpu': run_ssd(images_path, 'cpu')
        },
        'retinanet': {
            'cuda': run_retinanet(images_path, 'cuda'), 
            'cpu': run_retinanet(images_path, 'cpu') 
        }
    }
    return result

#load data
data_path = './data'
result_path = './result'
# Load the JSON file with image path

with open(data_path + '/labels.json', 'r') as json_file:
    labels = json.load(json_file)

total_data = len(labels)

modified_labels = {}
for label in labels:
    path = label['image_path']
    image_name = path.split("/")[-1]
    dir_path = path.replace(image_name, "")
    if dir_path in modified_labels:
        modified_labels[dir_path].append(image_name)
    else:
        modified_labels[dir_path] = [image_name]

for i in range(10):
    results = {}
    completed_data = 0
    for key in modified_labels:
        logging.info("Processing... " + key + " images")
        images_path = []
        for image_name in modified_labels[key]:
            images_path.append(data_path + key + image_name)
        result = run_detection(images_path)
        completed_data += len(images_path)
        results[key] = result
        logging.info("exp #" + str(i +1) + " DONE -> " + str((completed_data/total_data) * 100) + "%")

    json_results = json.dumps(results, indent=2)

    date_time = datetime.utcfromtimestamp(time()).strftime('%Y%m%d_%H:%M:%S_utc')
    result_json_name = 'raw_data_' + date_time + '.json'
    with open(result_path + "/exp_" + str(i + 1) + '_' + result_json_name, 'w') as json_file:
        json_file.write(json_results)

sys.stdout.close()

