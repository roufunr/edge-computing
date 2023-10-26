from ultralytics import YOLO


model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)
#metrics = model.val()  # evaluate model performance on the validation set
results = model("zidane.jpg")  # predict on an image
for result in results:
    boxes = result.boxes  # Boxes object for bbox outputs
    

    classes = boxes.cls.cpu().numpy().tolist()
    conf = boxes.conf.cpu().numpy().tolist()
    names_list = result.names

    print([names_list[class_idx] for class_idx in classes])
    print(conf)