import cv2
import os
import datetime
import time
import csv
import numpy
from skimage.metrics import structural_similarity as ssim
exp_start_time = time.time()
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
print(expeirment_id, "(MSE calculation) has been started...")

results = {}
experiment_folders_path = upscaled_images_folder_path + "/" + expeirment_id
resolutions_data = {}
for resolution in resolutions:
    resolution_folder_path = experiment_folders_path + "/" + resolution
    scaling_factors = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    scaling_data = {}
    for scaling_factor in scaling_factors:
        scaling_factor_folder_path = resolution_folder_path + "/" + str(scaling_factor)
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
            sample_data = []
            for i in range(1, SAMPLE_COUNT + 1):
                upscaled_image_path = method_name_folder_path + "/" + str(i) + ".bmp"
                upscaled_image = cv2.imread(upscaled_image_path)

                original_image_path = "./../images/original/captured_" + resolution + ".bmp"
                original_image = cv2.imread(original_image_path)

                # Ensure both images have the same dimensions
                height, width = original_image.shape[:2]  # Get the dimensions of the original image
                upscaled_image = cv2.resize(upscaled_image, (width, height))  # Resize the upscaled image

                # Calculate Mean Squared Error (MSE)
                mse = numpy.mean((upscaled_image - original_image)**2)

                # Calculate Peak Signal-to-Noise Ratio (PSNR)
                max_pixel_value = 255.0  # Assuming images are in 8-bit format
                psnr = 10 * numpy.log10((max_pixel_value ** 2) / mse)

                # Calculate Mean Absolute Error (MAE)
                mae = numpy.mean(numpy.abs(upscaled_image - original_image))
                sample = {
                    "MSE": mse,
                    "PSNR": psnr,
                    "MAE": mae
                }

                sample_data.append(sample)
            interpolations_data[method_name] = sample_data
        scaling_data[scaling_factor] = interpolations_data
    resolutions_data[resolution] = scaling_data

results = resolutions_data
exp_end_time = time.time()
total_time = (exp_end_time - exp_start_time)
print("Total time:", total_time, "seconds")




# report generation
report_experiment_path = "./../report/image_quality/" + expeirment_id
os.makedirs(report_experiment_path)
for resolution in resolutions:
    resolution_folder_path = report_experiment_path + "/" + resolution
    os.makedirs(resolution_folder_path)
    csv_mse_data = [('Scaling Factor', 'INTER_NEAREST (MSE)', 'INTER_LINEAR (MSE)', 'INTER_CUBIC (MSE)', 'INTER_AREA (MSE)', 'INTER_LANCZOS4 (MSE)')]
    csv_psnr_data = [('Scaling Factor', 'INTER_NEAREST (PSNR)', 'INTER_LINEAR (PSNR)', 'INTER_CUBIC (PSNR)', 'INTER_AREA (PSNR)', 'INTER_LANCZOS4 (PSNR)')]
    csv_mae_data = [('Scaling Factor', 'INTER_NEAREST (MAE)', 'INTER_LINEAR (MAE)', 'INTER_CUBIC (MAE)', 'INTER_AREA (MAE)', 'INTER_LANCZOS4 (MAE)')]
    scaling_factors = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    for scaling_factor in scaling_factors:
        # List of interpolation algorithms
        csv_mse_row = [scaling_factor]
        csv_psnr_row = [scaling_factor]
        csv_mae_row = [scaling_factor]
        interpolation_methods = {
            'INTER_NEAREST': cv2.INTER_NEAREST,
            'INTER_LINEAR': cv2.INTER_LINEAR,
            'INTER_CUBIC': cv2.INTER_CUBIC,
            'INTER_AREA': cv2.INTER_AREA,
            'INTER_LANCZOS4': cv2.INTER_LANCZOS4
        }
        for method_name, method in interpolation_methods.items():
            sum_of_mse = 0
            sum_of_psnr = 0
            sum_of_mae = 0
            for i in range(0, SAMPLE_COUNT):
                sum_of_mse += results[resolution][scaling_factor][method_name][i]["MSE"]
                sum_of_psnr += results[resolution][scaling_factor][method_name][i]["PSNR"]
                sum_of_mae += results[resolution][scaling_factor][method_name][i]["MAE"]
                
            avg_of_mse = sum_of_mse / SAMPLE_COUNT
            csv_mse_row.append(avg_of_mse)

            avg_of_psnr = sum_of_psnr / SAMPLE_COUNT
            csv_psnr_row.append(avg_of_psnr)

            avg_of_mae = sum_of_mae / SAMPLE_COUNT
            csv_mae_row.append(avg_of_mae)
            
        csv_mse_row = tuple(csv_mse_row)
        csv_mse_data.append(csv_mse_row)

        csv_psnr_row = tuple(csv_psnr_row)
        csv_psnr_data.append(csv_psnr_row)

        csv_mae_row = tuple(csv_mae_row)
        csv_mae_data.append(csv_mae_row)
    
    csv_mse_path = resolution_folder_path + "/" + "mse.csv"
    with open(csv_mse_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(csv_mse_data)
    
    csv_psnr_path = resolution_folder_path + "/" + "psnr.csv"
    with open(csv_psnr_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(csv_psnr_data)
    
    csv_mae_path = resolution_folder_path + "/" + "mae.csv"
    with open(csv_mae_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(csv_mae_data)
