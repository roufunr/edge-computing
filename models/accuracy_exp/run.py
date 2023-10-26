import cv2
import torch
import torchvision
from torchvision.models.detection import retinanet_resnet50_fpn, RetinaNet_ResNet50_FPN_Weights

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
    





    