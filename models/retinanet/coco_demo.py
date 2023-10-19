from pycocotools.coco import COCO

# Path to COCO dataset annotations (annotations_trainval2017.zip)
ann_file = 'path_to_annotations/instances_train2017.json'  # Replace with the actual path

# Initialize COCO object
coco = COCO(ann_file)

# Get the list of class names
class_names = [cat['name'] for cat in coco.loadCats(coco.getCatIds())]

# Print the class names
print(class_names)

