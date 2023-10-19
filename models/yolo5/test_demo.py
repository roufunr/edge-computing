import cv2
import torch
from PIL import Image
from time import time

import json
import copy

base_path = '/home/orin/Desktop/test_data'
# Load the JSON file with image path
with open(base_path + '/test_labels.json', 'r') as json_file:
    data = json.load(json_file)

all_images = []
for image in data:
    image_path = base_path + image['image_path']
    all_images.append(image_path)
    


# Model
model1 = torch.hub.load('ultralytics/yolov5', 'yolov5s')
model2 = torch.hub.load('ultralytics/yolov5', 'yolov5s')
models = {'cuda': model1.cuda(), 'cpu': model2.cpu()}

def run_object_detection_on_images(images_path, device): 
    images = []
    for image_path in images_path:         
        image = cv2.imread(image_path)[..., ::-1]
        images.append(image)
    # Inference
    strt = time() * 1000
    results = models[device](images, size=640) # batch of images
    end = time() * 1000
    return end - strt


print(run_object_detection_on_images(all_images, 'cuda'))
print(run_object_detection_on_images(all_images, 'cpu'))

