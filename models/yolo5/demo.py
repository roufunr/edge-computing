import cv2
import torch
from PIL import Image
from time import time


# Model
model1 = torch.hub.load('ultralytics/yolov5', 'yolov5s')
model2 = torch.hub.load('ultralytics/yolov5', 'yolov5s')
models = {'cuda': model1.cuda(), 'cpu': model2.cpu()}

# Images
for f in 'zidane.jpg', 'bus.jpg':
    torch.hub.download_url_to_file('https://ultralytics.com/images/' + f, f)  # download 2 images
im1 = cv2.imread('zidane.jpg')[..., ::-1]  # OpenCV image (BGR to RGB)  # PIL image
im2 = cv2.imread('bus.jpg')[..., ::-1]  # OpenCV image (BGR to RGB)

# Inference
strt = time() * 1000
results = models['cpu']([im1, im2], size=640) # batch of images
end = time() * 1000
# Results
results.print()
results.save()  # or .show()

results.xyxy[0]  # im1 predictions (tensor)
results.pandas().xyxy[0]  # im1 predictions (pandas)
print(results.pandas().xyxy[0]['name'],"\n", results.pandas().xyxy[0]['confidence'])
#      xmin    ymin    xmax   ymax  confidence  class    name
# 0  749.50   43.50  1148.0  704.5    0.874023      0  person
# 1  433.50  433.50   517.5  714.5    0.687988     27     tie
# 2  114.75  195.75  1095.0  708.0    0.624512      0  person
# 3  986.00  304.00  1028.0  420.0    0.286865     27     tie

print('inference time', end - strt)

