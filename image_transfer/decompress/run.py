import os
import sys
import json
import cv2
import time

data_base_path = "/home/rouf-linux/data"
compressed_image_base_path = data_base_path + "/compressed"
decompressed_image_base_path = data_base_path + "/decompressed"
os.makedirs(decompressed_image_base_path, exist_ok=True)

resolutions = ['160x90', '160x100', '160x120', '320x180', '320x200', '320x240', '480x270', '480x300', '480x360', '640x360', '640x400', '640x480', '800x450', '800x500', '800x600', '1024x576', '1024x640', '1024x768', '1280x720', '1280x800', '1280x960', '1440x900', '1440x1080', '1920x1080']
frames = [1, 2, 4, 8, 16, 32]
total_experiment = 1
scaling_factors = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
interpolation_methods = {
    'INTER_NEAREST': cv2.INTER_NEAREST,
    'INTER_LINEAR': cv2.INTER_LINEAR,
    'INTER_CUBIC': cv2.INTER_CUBIC,
    'INTER_AREA': cv2.INTER_AREA,
    'INTER_LANCZOS4': cv2.INTER_LANCZOS4
}
ip_methods = ['INTER_NEAREST', 'INTER_LINEAR', 'INTER_CUBIC', 'INTER_AREA', 'INTER_LANCZOS4']
ip_methods_name_mapper = {
    'INTER_NEAREST': "Nearest",
    'INTER_LINEAR': "Linear",
    'INTER_CUBIC': "Inter-Cubic",
    'INTER_AREA': "Area",
    'INTER_LANCZOS4': "Lanczos4"
}


def upscale(image_path, scaling_factor, scaling_method): 
    image = cv2.imread(image_path)
    start_time = time.time() * 1000
    upscaled_image = cv2.resize(image, None, fx=1/scaling_factor, fy=1/scaling_factor, interpolation=scaling_method)
    end_time = time.time() * 1000
    elapsed_time = end_time - start_time
    return upscaled_image, elapsed_time

def save_processed_image(cv2_image, save_path, image_name):
    os.makedirs(save_path, exist_ok=True)
    cv2.imwrite(save_path + "/" + image_name, cv2_image)
    return "DONE"

def save_data_as_json(data, json_path):
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def run_experiment(exp_id):
    exp_dict = {}
    for ip_method in ip_methods:
        for scaling_factor in scaling_factors:
            for resolution in resolutions:
                for frame in frames:
                    frame_start_id = frame - 1
                    elapsed_time_sum = 0
                    for i in range(frame):
                        image_path = compressed_image_base_path + "/" + ip_method + "/" + str(scaling_factor) + "/" + resolution + "/" + str(frame) + "/" + str(frame_start_id + i) + ".bmp"
                        upscaled_cv2_image, elapsed_time = upscale(image_path, scaling_factor, interpolation_methods[ip_method])
                        elapsed_time_sum += elapsed_time
                        save_processed_image(upscaled_cv2_image, decompressed_image_base_path + "/" + str(exp_id) + "/" + ip_method + "/" + str(scaling_factor) + "/" + resolution + "/" + str(frame), str(frame_start_id + i) + ".bmp")
                    key = str(exp_id) + "/" + ip_method + "/" + str(scaling_factor) + "/" + resolution + "/" + str(frame)
                    print(key + "   DONE!")
                    exp_dict[key] = elapsed_time_sum     
    save_data_as_json(exp_dict, "/home/rouf-linux/edge-computing/image_transfer/decompress/result" + "/" + str(exp_id) + ".json")

for exp_id in range(total_experiment):
    run_experiment(exp_id)


    
