import torch
import logging

logging.basicConfig(filename='object_detection_calculate_metrics.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



ssd_model = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_ssd')
ssd_utils = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_ssd_processing_utils')
ssd_model.to('cuda')
ssd_model.eval()
classes_to_labels = ssd_utils.get_coco_object_dictionary()

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

