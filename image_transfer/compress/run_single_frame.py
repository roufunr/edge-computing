import os
import json
import cv2
import time

data_base_path = "/home/rouf-linux/single-frame-data"
original_image_base_path = data_base_path + "/original"
compressed_image_base_path = data_base_path + "/compressed"
resolutions = {
    "cam1": ['160x90', '160x100', '160x120', '240x180', '320x180', '320x200', '320x240', '480x270', '480x300', '480x360', '640x360', '640x400', '640x480', '800x450', '800x500', '800x600', '1024x576', '1024x640', '1024x768', '1280x720', '1280x800', '1280x960', '1440x900', '1440x1080', '1920x1080'],
    "cam2": ['160x90', '160x100', '160x120', '240x180', '320x180', '320x200', '320x240', '480x270', '480x300', '480x360', '640x360', '640x400', '640x480', '800x450', '800x500', '800x600', '1024x576', '1024x640', '1024x768', '1280x720', '1280x800', '1280x960', '1440x900', '1440x1080', '1920x1080'],
    "cam3": ['160x90', '160x120', '176x144', '240x180', '320x180', '320x240', '480x270', '480x360', '640x360', '640x480', '800x450', '800x600', '1024x640', '1024x768', '1280x720', '1280x800', '1280x960'],
    "cam4": ['streamid_1/quality_1', 'streamid_1/quality_2', 'streamid_1/quality_3', 'streamid_1/quality_4', 'streamid_1/quality_5', 'streamid_0/quality_1', 'streamid_0/quality_2', 'streamid_0/quality_3', 'streamid_0/quality_4', 'streamid_0/quality_5']
}
total_experiment = 11
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
    'INTER_CUBIC': "Cubic",
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
    for cam in resolutions:
        for resolution in resolutions[cam]:
            for ip_method in interpolation_methods:
                for scaling_factor in scaling_factors:
                    key = cam + "/" + resolution + "/" + ip_method + "/" + str(scaling_factor)
                    scaled_image_dir = compressed_image_base_path + "/" + key
                    os.makedirs(scaled_image_dir, exist_ok=True)
                    original_image_path = original_image_base_path + "/" + cam + "/" + resolution
                    scaled_image_name = "0."
                    if cam == "cam4": 
                        original_image_path += "/0.jpeg"
                        scaled_image_name += "jpeg"
                    else: 
                        original_image_path += "/0.bmp"
                        scaled_image_name += "bmp"
                    
                    d_image, elapsed_time = downscale(original_image_path, scaling_factor, interpolation_methods[ip_method])
                    exp_dict[key] = elapsed_time
                    print(key, "Done")
                    save_processed_image(d_image, scaled_image_dir, scaled_image_name)
    # save_data_as_json(exp_dict, "/home/rouf-linux/edge-computing/image_transfer/compress/single_frame_result/" + str(exp_id) + ".json")

for exp_id in range(1):
    run_experiment(exp_id)


    
