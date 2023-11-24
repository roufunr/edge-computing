from imageai.Detection import ObjectDetection
from time import time

home_directory = "/home/jtx2"
detector = ObjectDetection()
# detector.useCPU()
detector.setModelTypeAsRetinaNet()
detector.setModelPath(home_directory + "/retinanet_model.pth")  # Specify the path to the RetinaNet model
detector.loadModel()

# Detect objects in an image
start_time = time() * 1000
detections = detector.detectObjectsFromImage(input_image= "/home/jtx2/data/original/cam1/240x180/0.bmp")
end_time = time() * 1000

print(end_time - start_time)

for detection in detections:
    print(detection["name"], " : ", detection["percentage_probability"])
