import cv2
import os
import datetime
import time
import csv
exp_start_time = time.time()
downscaled_images_folder_path = "./../images/downscaled"
upscaled_images_folder_path = "./../images/upscaled"
SAMPLE_COUNT = 10 

resolutions = [
    '1920x1080',
    '1440x1080',
    '1440x900',
    '1280x960',
    '1280x800',
    '1280x720',
    '1024x768',
    '1024x640',
    '1024x576',
    '800x600',
    '800x500',
    '800x450',
    '640x480',
    '640x400',
    '640x360',
    '480x360',
    '480x300',
    '480x270',
    '320x240',
    '320x200',
    '320x180',
    '240x180',
    '160x120',
    '160x100',
    '160x90'
]

original_images_size_kb = [
    6075.05,
    4556.30,
    3796.93,
    3600.05,
    3000.05,
    2700.05,
    2304.05,
    1920.05,
    1728.05,
    1406.30,
    1171.93,
    1054.74,
    900.05,
    750.05,
    675.05,
    506.30,
    421.93,
    379.74,
    225.05,
    187.55,
    168.80,
    126.62,
    56.30,
    46.93,
    42.24
]

def getCurrentDateTimeString():
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d___%H:%M:%S")
    return formatted_datetime

expeirment_id = '2023-08-22___17:08:20'
print(expeirment_id, "(upscaling) has been started...")

results = {}
experiment_folders_path = upscaled_images_folder_path + "/" + expeirment_id
os.makedirs(experiment_folders_path)
resolutions_data = {}
for resolution in resolutions:
    resolution_folder_path = experiment_folders_path + "/" + resolution
    os.makedirs(resolution_folder_path)
    scaling_factors = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    scaling_data = {}
    for scaling_factor in scaling_factors:
        scaling_factor_folder_path = resolution_folder_path + "/" + str(scaling_factor)
        os.makedirs(scaling_factor_folder_path)
        # List of interpolation algorithms
        interpolation_methods = {
            'INTER_NEAREST': cv2.INTER_NEAREST,
            'INTER_LINEAR': cv2.INTER_LINEAR,
            'INTER_CUBIC': cv2.INTER_CUBIC,
            'INTER_AREA': cv2.INTER_AREA,
            'INTER_LANCZOS4': cv2.INTER_LANCZOS4
        }

        interpolations_data = {}
        for method_name, method in interpolation_methods.items():
            method_name_folder_path = scaling_factor_folder_path + "/" + method_name
            os.makedirs(method_name_folder_path)
            sample_data = []
            for i in range(1, SAMPLE_COUNT + 1):
                image_path = method_name_folder_path.replace("upscaled", "downscaled") + "/" + str(i) + ".bmp"
                image = cv2.imread(image_path)

                start_time = time.time() * 1000
                upscaled_image = cv2.resize(image, None, fx=1/scaling_factor, fy=1/scaling_factor, interpolation=method)
                end_time = time.time() * 1000

                upscale_filename = f'{method_name_folder_path}/{i}.bmp'
                
                cv2.imwrite(upscale_filename, upscaled_image)

                upscale_size_mb = os.path.getsize(upscale_filename) / (1024)
                upscale_image_elapsed_time = end_time - start_time
                sample = {
                    "image_size_kb": upscale_size_mb,
                    "elapsed_time": upscale_image_elapsed_time
                }
                sample_data.append(sample)
            interpolations_data[method_name] = sample_data
        scaling_data[scaling_factor] = interpolations_data
    resolutions_data[resolution] = scaling_data

results = resolutions_data
exp_end_time = time.time()
total_time = (exp_end_time - exp_start_time)
print("Total time:", total_time, "seconds")




#report generation
report_experiment_path = "./../report/upscale/" + expeirment_id
os.makedirs(report_experiment_path)
for resolution in resolutions:
    resolution_folder_path = report_experiment_path + "/" + resolution
    os.makedirs(resolution_folder_path)
    csv_time_data = [('Scaling Factor', 'INTER_NEAREST (ms)', 'INTER_LINEAR (ms)', 'INTER_CUBIC (ms)', 'INTER_AREA (ms)', 'INTER_LANCZOS4 (ms)')]
    csv_size_data = [('Scaling Factor', 'INTER_NEAREST (kb)', 'INTER_LINEAR (kb)', 'INTER_CUBIC (kb)', 'INTER_AREA (kb)', 'INTER_LANCZOS4 (kb)')]
    scaling_factors = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    for scaling_factor in scaling_factors:
        # List of interpolation algorithms
        csv_time_row = [scaling_factor]
        csv_size_row = [scaling_factor]
        interpolation_methods = {
            'INTER_NEAREST': cv2.INTER_NEAREST,
            'INTER_LINEAR': cv2.INTER_LINEAR,
            'INTER_CUBIC': cv2.INTER_CUBIC,
            'INTER_AREA': cv2.INTER_AREA,
            'INTER_LANCZOS4': cv2.INTER_LANCZOS4
        }
        for method_name, method in interpolation_methods.items():
            sum_of_sizes = 0
            sum_of_time = 0
            for i in range(0, SAMPLE_COUNT):
                sum_of_sizes += results[resolution][scaling_factor][method_name][i]["image_size_kb"]
                sum_of_time += results[resolution][scaling_factor][method_name][i]["elapsed_time"]
            avg_size_kb = sum_of_sizes / SAMPLE_COUNT
            avg_time = sum_of_time /SAMPLE_COUNT
            csv_time_row.append(avg_time)
            csv_size_row.append(avg_size_kb)
        csv_size_row = tuple(csv_size_row)
        csv_time_row = tuple(csv_time_row)

        csv_time_data.append(csv_time_row)
        csv_size_data.append(csv_size_row)
    
    csv_time_path = resolution_folder_path + "/" + "time.csv"
    with open(csv_time_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(csv_time_data)
    
    csv_size_path = resolution_folder_path + "/" + "kb.csv"
    with open(csv_size_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(csv_size_data)
