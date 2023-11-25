import json
import csv


resolutions = {
    "cam1": ['160x90', '160x100', '160x120', '240x180', '320x180', '320x200', '320x240', '480x270', '480x300', '480x360', '640x360', '640x400', '640x480', '800x450', '800x500', '800x600', '1024x576', '1024x640', '1024x768', '1280x720', '1280x800', '1280x960', '1440x900', '1440x1080', '1920x1080'],
    "cam2": ['160x90', '160x100', '160x120', '240x180', '320x180', '320x200', '320x240', '480x270', '480x300', '480x360', '640x360', '640x400', '640x480', '800x450', '800x500', '800x600', '1024x576', '1024x640', '1024x768', '1280x720', '1280x800', '1280x960', '1440x900', '1440x1080', '1920x1080'],
    "cam3": ['160x90', '160x120', '176x144', '240x180', '320x180', '320x240', '480x270', '480x360', '640x360', '640x480', '800x450', '800x600', '1024x640', '1024x768', '1280x720', '1280x800', '1280x960'],
    "cam4": ['streamid_1/quality_1', 'streamid_1/quality_2', 'streamid_1/quality_3', 'streamid_1/quality_4', 'streamid_1/quality_5', 'streamid_0/quality_1', 'streamid_0/quality_2', 'streamid_0/quality_3', 'streamid_0/quality_4', 'streamid_0/quality_5']
}

scaling_factors = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
ip_methods = ['INTER_NEAREST', 'INTER_LINEAR', 'INTER_CUBIC', 'INTER_AREA', 'INTER_LANCZOS4']

ip_methods_name_mapper = {
    'INTER_NEAREST': "Nearest",
    'INTER_LINEAR': "Linear",
    'INTER_CUBIC': "Cubic",
    'INTER_AREA': "Area",
    'INTER_LANCZOS4': "Lanczos4"
}

def load_json(json_path):
    with open(json_path, 'r') as file:
        loaded_data = json.load(file)
        return loaded_data

def save_to_json(new_json_path, data):
    with open(new_json_path, 'w') as file:
        json.dump(data, file)

def load_data():
    data = []
    for i in range(1, 11):
        json_data = load_json("/home/rouf-linux/edge-computing/tx2i_report_generation/raw_data/decompression_time/"+ str(i) +".json")
        data.append(json_data)
    return data

def calculate_median(samples):
    sorted_samples = sorted(samples)
    n = len(sorted_samples)
    if n % 2 == 0:
        middle = n // 2
        median = (sorted_samples[middle - 1] + sorted_samples[middle]) / 2
    else:
        median = sorted_samples[n // 2]
    return median
    
def generate_median(data): 
    median_data = {}
    for cam in resolutions:
        for resolution in resolutions[cam]:
            for ip_method in ip_methods:
                for scaling_factor in scaling_factors:
                    key = cam + "/" + resolution + "/" + ip_method + "/" + str(scaling_factor)
                    samples = [data[i][key] for i in range(10)]
                    median = calculate_median(samples)
                    median_data[key] = median
    # print(median_data)
    return median_data

def create_csv_from_2d_list(data, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def generate_csv(median):
    for cam in resolutions:
        rows = []
        header = []
        for ip_method in ip_methods:
            header.append(ip_methods_name_mapper[ip_method])
            for scaling_factor in scaling_factors:
                header.append(scaling_factor)
            header.append("         ")
        rows.append(header)    
        for resolution in resolutions[cam]:
            row = []
            for ip_method in ip_methods:
                row.append(resolution)
                for scaling_factor in scaling_factors:
                    key = cam + "/" + resolution + "/" + ip_method + "/" + str(scaling_factor)
                    row.append(round(median[key],4))
                row.append("         ")
            rows.append(row)
        create_csv_from_2d_list(rows, "/home/rouf-linux/edge-computing/tx2i_report_generation/csv/decompression_time/" + cam + ".csv")
            
    
    
# "cam1/160x90/INTER_NEAREST/0.1": 0.009033203125,
data = load_data()
median = generate_median(data)
generate_csv(median)