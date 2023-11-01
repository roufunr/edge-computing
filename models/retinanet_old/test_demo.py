import cv2
from PIL import Image
import torch
import torchvision
import json
import os
from torchvision.models.detection import retinanet_resnet50_fpn, RetinaNet_ResNet50_FPN_Weights
from time import time




base_path = '/home/orin/Desktop/test_data'
# Load the JSON file with image path
with open(base_path + '/test_labels.json', 'r') as json_file:
    data = json.load(json_file)
    
    
    
    
# Load the pre-trained RetinaNet model
model = [retinanet_resnet50_fpn(weights=RetinaNet_ResNet50_FPN_Weights.DEFAULT), retinanet_resnet50_fpn(weights=RetinaNet_ResNet50_FPN_Weights.DEFAULT)]
trained_model = {'cuda': model[0].to("cuda"), 'cpu': model[1].to("cpu")}
trained_model['cuda'].eval()
trained_model['cpu'].eval()


classes = {
    "indexToClass": {
        "1": "person",
        "2": "bicycle",
        "3": "car",
        "4": "motorcycle",
        "5": "airplane",
        "6": "bus",
        "7": "train",
        "8": "truck",
        "9": "boat",
        "10": "traffic light",
        "11": "fire hydrant",
        "13": "stop sign",
        "14": "parking meter",
        "15": "bench",
        "16": "bird",
        "17": "cat",
        "18": "dog",
        "19": "horse",
        "20": "sheep",
        "21": "cow",
        "22": "elephant",
        "23": "bear",
        "24": "zebra",
        "25": "giraffe",
        "27": "backpack",
        "28": "umbrella",
        "31": "handbag",
        "32": "tie",
        "33": "suitcase",
        "34": "frisbee",
        "35": "skis",
        "36": "snowboard",
        "37": "sports ball",
        "38": "kite",
        "39": "baseball bat",
        "40": "baseball glove",
        "41": "skateboard",
        "42": "surfboard",
        "43": "tennis racket",
        "44": "bottle",
        "46": "wine glass",
        "47": "cup",
        "48": "fork",
        "49": "knife",
        "50": "spoon",
        "51": "bowl",
        "52": "banana",
        "53": "apple",
        "54": "sandwich",
        "55": "orange",
        "56": "broccoli",
        "57": "carrot",
        "58": "hot dog",
        "59": "pizza",
        "60": "donut",
        "61": "cake",
        "62": "chair",
        "63": "couch",
        "64": "potted plant",
        "65": "bed",
        "67": "dining table",
        "70": "toilet",
        "72": "tv",
        "73": "laptop",
        "74": "mouse",
        "75": "remote",
        "76": "keyboard",
        "77": "cell phone",
        "78": "microwave",
        "79": "oven",
        "80": "toaster",
        "81": "sink",
        "82": "refrigerator",
        "84": "book",
        "85": "clock",
        "86": "vase",
        "87": "scissors",
        "88": "teddy bear",
        "89": "hair drier",
        "90": "toothbrush"
    }
}



def run_object_detection_on_single_image(image_path, device): 
    #print('Working on ', image_path)
    # Read the image
    image = cv2.imread(image_path)
    # Transform and preprocess the image
    transform = torchvision.transforms.Compose([torchvision.transforms.ToTensor(), torchvision.transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.299, 0.224, 0.225])])
    input_image = transform(image)
    input_image = input_image.unsqueeze(0)
    input_image = input_image.to(device)

    # Perform object detection
    with torch.no_grad():
        start_time = time() * 1000
        prediction = trained_model[device](input_image)
        end_time = time() * 1000
    
    elapsed_time = end_time - start_time
    return elapsed_time 
    #print('elapsed_time', elapsed_time)
    # Extract detection results
    #boxes = prediction[0]['boxes']
    #scores = prediction[0]['scores']
    #labels = prediction[0]['labels']
    
    
    
    #min_conf = 1.00
    #for obj in image_data['objects']:
    #    if min_conf > obj['confidence']:
    #        min_conf = obj['confidence']
    
    #print('\n\ndetected label\n')
    # Annotate the image with detected objects
    #for box, score, label in zip(boxes, scores, labels):
    #    box = box.int().tolist()
    #    label_name = classes['indexToClass'][str(label.item())]
    #    confidence = score.item()
    #    if confidence >=  min_conf:
    #        print(label_name)
    

def run_object_detection_on_multiple_images(images_path, device): 
    #print('Working on ', images_path)
    # Read the image
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
            prediction = trained_model[device](input_image)
            end_time = time() * 1000
    
        elapsed_time = end_time - start_time 
        #print('elapsed_time', elapsed_time)
        total_elapsed_time += elapsed_time
    return total_elapsed_time



all_images = []
for image in data:
    image_path = base_path + image['image_path']
    all_images.append(image_path)
run_object_detection_on_single_image(all_images[0], "cuda")
run_object_detection_on_single_image(all_images[0], "cpu")
print(run_object_detection_on_multiple_images(all_images, "cuda"))
print(run_object_detection_on_multiple_images(all_images, "cpu"))




