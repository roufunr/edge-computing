import csv
import os
import json

raw_results_base_path = "/Users/abdurrouf/edge-computing/image_transfer/report_generation/raw_results"
parts = ["compression", "decompression", "transfer"]
transfer_image_type = ["original", "compressed"]
transfer_time_type = ["transfer_time", "disk_write_time", "response_time"]
resolutions = ['160x90', '160x100', '160x120', '320x180', '320x200', '320x240', '480x270', '480x300', '480x360', '640x360', '640x400', '640x480', '800x450', '800x500', '800x600', '1024x576', '1024x640', '1024x768', '1280x720', '1280x800', '1280x960', '1440x900', '1440x1080', '1920x1080']
frames = [1, 2, 4, 8, 16, 32]
total_experiment = 10
scaling_factors = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
ip_methods = ['INTER_NEAREST', 'INTER_LINEAR', 'INTER_CUBIC', 'INTER_AREA', 'INTER_LANCZOS4']
ip_methods_name_mapper = {
    'INTER_NEAREST': "Nearest",
    'INTER_LINEAR': "Linear",
    'INTER_CUBIC': "Cubic",
    'INTER_AREA': "Area",
    'INTER_LANCZOS4': "Lanczos4"
}

def generateKeys(image_type):
    keys = []
    if image_type == "original":
        for resolution in resolutions:
            for frame in frames:
                keys.append(resolution + "/" + str(frame))
    else: 
        for ip_method in ip_methods:
            for scaling_factor in scaling_factors:
                for resolution in resolutions:
                    for frame in frames:
                        keys.append(ip_method + "/" + str(scaling_factor) + "/" + resolution + "/" + str(frame))
    return keys

def write_2d_list_to_csv(data,file_path, filename):
    os.makedirs(file_path, exist_ok=True)
    
    try:
        with open(file_path + "/" + filename, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(data)
        print(f"CSV file '{file_path}' has been successfully created with the 2D list data.")
    except Exception as e:
        print(f"An error occurred: {e}")

original_images_keys = generateKeys("original")
compressed_images_keys = generateKeys("compressed")

def load_json(json_path):
    with open(json_path, 'r') as json_file:
        json_data = json.load(json_file)
    return json_data

data = load_json("/Users/abdurrouf/edge-computing/image_transfer/report_generation/raw_results/median_data.json")

#transfer
#orignal
rows = []
header = ["orignal"]
header += frames
rows.append(header)
for resolution in resolutions:
    row = [resolution]
    for frame in frames:
        row.append(round(data["transfer"]["original"][resolution + "/" + str(frame)]["response_time"], 3))
    rows.append(row)
write_2d_list_to_csv(rows, "/Users/abdurrouf/edge-computing/image_transfer/report_generation/csv" + "/" + "transfer" + "/" + "original", "original.csv")
#compressed
for ip_method in ip_methods:
    for scaling_factor in scaling_factors:
        rows = []
        header = [ip_methods_name_mapper[ip_method] + "_" + str(scaling_factor)]
        header += frames
        rows.append(header)
        for resolution in resolutions:
            row = [resolution]
            for frame in frames:
                row.append(round(data["transfer"]["compressed"][ip_method+"/" + str(scaling_factor)  + "/" + resolution + "/" + str(frame)]["response_time"], 3))
            rows.append(row)
        write_2d_list_to_csv(rows, "/Users/abdurrouf/edge-computing/image_transfer/report_generation/csv" + "/" + "transfer" + "/" + "compressed" + "/" + ip_method, str(scaling_factor) + ".csv")
###################
#compression
for ip_method in ip_methods:
    for scaling_factor in scaling_factors:
        rows = []
        header = [ip_methods_name_mapper[ip_method] + "_" + str(scaling_factor)]
        header += frames
        rows.append(header)
        for resolution in resolutions:
            row = [resolution]
            for frame in frames:
                row.append(round(data["compression"][ip_method+"/" + str(scaling_factor)  + "/" + resolution + "/" + str(frame)], 3))
            rows.append(row)
        write_2d_list_to_csv(rows, "/Users/abdurrouf/edge-computing/image_transfer/report_generation/csv" + "/" + "compression" + "/" + ip_method, str(scaling_factor) + ".csv")


#decompression
for ip_method in ip_methods:
    for scaling_factor in scaling_factors:
        rows = []
        header = [ip_methods_name_mapper[ip_method] + "_" + str(scaling_factor)]
        header += frames
        rows.append(header)
        for resolution in resolutions:
            row = [resolution]
            for frame in frames:
                row.append(round(data["decompression"][ip_method+"/" + str(scaling_factor)  + "/" + resolution + "/" + str(frame)], 3))
            rows.append(row)
        write_2d_list_to_csv(rows, "/Users/abdurrouf/edge-computing/image_transfer/report_generation/csv" + "/" + "decompression" + "/" + ip_method, str(scaling_factor) + ".csv")



