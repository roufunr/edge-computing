import torch
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

utils = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_ssd_processing_utils')

# Load the SSD model once
ssd_model = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_ssd')

ssd_model_cuda = copy.deepcopy(ssd_model).to('cuda')
ssd_model_cuda.eval()

ssd_model_cpu = copy.deepcopy(ssd_model).to('cpu')
ssd_model_cpu.eval()

models = {'cuda': ssd_model_cuda, 'cpu': ssd_model_cpu}

def run_object_detection_on_images(images_path, device): 
    inputs = [utils.prepare_input(image) for image in all_images]
    tensor = utils.prepare_tensor(inputs).to(device)
    with torch.no_grad():
        start_time = time() * 1000
        detections_batch = models[device](tensor)
        end_time = time() * 1000

    return end_time - start_time

print(run_object_detection_on_images(all_images, 'cuda'))
print(run_object_detection_on_images(all_images, 'cpu'))

