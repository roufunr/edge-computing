import os
import sys
import json
import cv2
import time

data_base_path = "/home/rouf-linux/compression_data"
original_image_base_path = data_base_path + "/original"
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


def downscale(image_path, scaling_factor, scaling_method): 
    image = cv2.imread(image_path)
    start_time = time.time() * 1000
    downscaled_image = cv2.resize(image, None, fx=scaling_factor, fy=scaling_factor, interpolation=scaling_method)
    end_time = time.time() * 1000
    elapsed_time = end_time - start_time
    return downscaled_image, elapsed_time

def save_processed_image(cv2_image, save_path, image_name):
    os.makedirs(save_path, exist_ok=True)
    cv2.imwrite(save_path + "/" + image_name, cv2_image)
    return "DONE"

def save_data_as_json(data, json_path):
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def run_experiment(exp_id):
    exp_dict = {}
    for resolution in resolutions:
        for frame_idx in range(len(frames)):
            image_list = []
            first_image_id = frames[frame_idx] - 1
            for i in range(frames[frame_idx]):
                image_list.append(first_image_id + i)
            
            for ip_method in interpolation_methods:
                for scaling_factor in scaling_factors:
                    original_image_path = original_image_base_path + "/" + resolution + "/" + str(frames[frame_idx]) 
                    image_save_base_path = data_base_path + "/" + str(exp_id) + "/" + ip_method + "/" + str(scaling_factor) + "/" + resolution + "/" + str(frames[frame_idx])
                    elapsed_time_sum = 0
                    for image in image_list:
                        image_path = original_image_path + "/" + str(image) + ".bmp"
                        downscaled_cv2_image, elapsed_time = downscale(image_path, scaling_factor=scaling_factor, scaling_method=interpolation_methods[ip_method])
                        elapsed_time_sum += elapsed_time
                        save_processed_image(downscaled_cv2_image, image_save_base_path, str(image) + ".bmp")
                    exp_dict[image_save_base_path] = elapsed_time_sum
                    print("DONE ::: " + image_save_base_path)
    save_data_as_json(exp_dict, "/home/rouf-linux/edge-computing/image_transfer/compress/result_nov_17/" + str(exp_id) + ".json")

for exp_id in range(total_experiment):
    run_experiment(exp_id)


    
