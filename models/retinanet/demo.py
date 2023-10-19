import cv2
import torch
import torchvision
from torchvision.models.detection import retinanet_resnet50_fpn, RetinaNet_ResNet50_FPN_Weights


model = retinanet_resnet50_fpn(weights=RetinaNet_ResNet50_FPN_Weights.DEFAULT)
model = model.to("cuda:0")
model.eval()

categories = RetinaNet_ResNet50_FPN_Weights.DEFAULT
print(categories)

image = cv2.imread('bus.jpg')

transform = torchvision.transforms.Compose([torchvision.transforms.ToTensor(), torchvision.transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.299, 0.224, 0.225])])

input_image = transform(image)
input_image=input_image.unsqueeze(0)
input_image=input_image.to("cuda:0")

with torch.no_grad():
    prediction = model(input_image)


boxes = prediction[0]['boxes']
scores = prediction[0]['scores']
labels = prediction[0]['labels']

for box, score, label in zip(boxes, scores, labels): 
    box = box.int().tolist()
    label_name = f'Class {label.item()}'
    confidence = score.item()
    cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
    cv2.putText(image, f'{label_name}: {confidence: .2f}', (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
#Display
cv2.imshow('Object Detection', image)    
cv2.waitKey(0)
cv2.destroyAllWindows()    
