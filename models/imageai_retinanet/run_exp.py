from imageai.Detection import ObjectDetection
from time import time
import logging
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  
file_handler = logging.FileHandler('logfile.log')  
file_handler.setLevel(logging.DEBUG)  
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

home_directory = "/home/jtx2"

resolutions = {
    "cam1": ['160x90', '160x100', '160x120', '240x180', '320x180', '320x200', '320x240', '480x270', '480x300', '480x360', '640x360', '640x400', '640x480', '800x450', '800x500', '800x600', '1024x576', '1024x640', '1024x768', '1280x720', '1280x800', '1280x960', '1440x900', '1440x1080', '1920x1080'],
    "cam2": ['160x90', '160x100', '160x120', '240x180', '320x180', '320x200', '320x240', '480x270', '480x300', '480x360', '640x360', '640x400', '640x480', '800x450', '800x500', '800x600', '1024x576', '1024x640', '1024x768', '1280x720', '1280x800', '1280x960', '1440x900', '1440x1080', '1920x1080'],
    "cam3": ['160x90', '160x120', '176x144', '240x180', '320x180', '320x240', '480x270', '480x360', '640x360', '640x480', '800x450', '800x600', '1024x640', '1024x768', '1280x720', '1280x800', '1280x960'],
    "cam4": ['streamid_1/quality_1', 'streamid_1/quality_2', 'streamid_1/quality_3', 'streamid_1/quality_4', 'streamid_1/quality_5', 'streamid_0/quality_1', 'streamid_0/quality_2', 'streamid_0/quality_3', 'streamid_0/quality_4', 'streamid_0/quality_5']
}

def get_model():
    detector = ObjectDetection()
    # detector.useCPU()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath(home_directory + "/retinanet_model.pth")  # Specify the path to the RetinaNet model
    detector.loadModel()
    logger.info("Loaded model!")
    return detector


def run_detection(model, image_path):
    start_time = time() * 1000
    model.detectObjectsFromImage(input_image= image_path)
    end_time = time() * 1000
    return end_time - start_time
    
def run_exp(exp_id):
    exp_data = {}
    total_data = 0
    done_data = 0
    for cam in resolutions:
        total_data += len(resolutions[cam])
    
    model = get_model()
    for cam in resolutions:
        for resolution in resolutions[cam]:
            key = cam + "/" + resolution
            image_path = home_directory + "/data/original/" + key + "/0.jpeg"
            elapsed_time = run_detection(model, image_path)
            exp_data[key] = elapsed_time
            done_data += 1
            logger.info(str(exp_id) + " :::: " + str((done_data/total_data) * 100) + "% DONE!")
    
    return exp_data

def save_as_json(data, path):
    json_string = json.dumps(data)
    with open(path, 'w') as json_file:
        json_file.write(json_string) 
    
    logger.info("Generated :::: " + path + " !")          
            
            
for i in range(11):
    data = run_exp(i)
    save_as_json(data, "/home/rouf-linux/edge-computing/models/imageai_retinanet/results/" + str(i) + ".json")



# start_time = time() * 1000
# detections = detector.detectObjectsFromImage(input_image= "/home/jtx2/data/original/cam1/240x180/0.bmp")
# end_time = time() * 1000
# print(end_time - start_time)

# for detection in detections:
#     print(detection["name"], " : ", detection["percentage_probability"])