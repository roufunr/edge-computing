import torch
from time import time
ssd_model = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_ssd')
utils = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_ssd_processing_utils')
ssd_model.to('cuda')
ssd_model.eval()
# uris = [
#     'http://images.cocodataset.org/val2017/000000397133.jpg',
#     'http://images.cocodataset.org/val2017/000000037777.jpg',
#     'http://images.cocodataset.org/val2017/000000252219.jpg'
# ]
uris = [
    'donut.jpg'
]
inputs = [utils.prepare_input(uri) for uri in uris]
tensor = utils.prepare_tensor(inputs)
with torch.no_grad():
    start_time = time()
    detections_batch = ssd_model(tensor)
    end_time = time()

print(end_time - start_time)
results_per_input = utils.decode_results(detections_batch)
best_results_per_input = [utils.pick_best(results, 0.00) for results in results_per_input]
classes_to_labels = utils.get_coco_object_dictionary()


from matplotlib import pyplot as plt
import matplotlib.patches as patches

for image_idx in range(len(best_results_per_input)):
    #fig, ax = plt.subplots(1)
    # Show original, denormalized image...
    image = inputs[image_idx] / 2 + 0.5
    #ax.imshow(image)
    # ...with detections
    bboxes, classes, confidences = best_results_per_input[image_idx]
    for idx in range(len(bboxes)):
        # left, bot, right, top = bboxes[idx]
        # x, y, w, h = [val * 300 for val in [left, bot, right - left, top - bot]]
        # rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='r', facecolor='none')
        # ax.add_patch(rect)
        print(classes_to_labels[classes[idx] - 1], confidences[idx])
        # ax.text(x, y, "{} {:.0f}%".format(classes_to_labels[classes[idx] - 1], confidences[idx]*100), bbox=dict(facecolor='white', alpha=0.5))
# plt.show()

