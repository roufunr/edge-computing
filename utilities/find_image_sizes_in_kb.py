from PIL import Image
import os
import csv

original_image_base_path = "/home/rouf-linux/compression_data/original"
compressed_image_base_path = "/home/rouf-linux/compression_data/compressed"
# cam1 
resolutions = ['160x90', '160x100', '160x120', '240x180', '320x180', '320x200', '320x240', '480x270', '480x300', '480x360', '640x360', '640x400', '640x480', '800x450', '800x500', '800x600', '1024x576', '1024x640', '1024x768', '1280x720', '1280x800', '1280x960', '1440x900', '1440x1080', '1920x1080']
scaling_factor = 0.7
ip_methods_name_mapper = {
    'INTER_NEAREST': "Nearest",
    'INTER_LINEAR': "Linear",
    'INTER_CUBIC': "Cubic",
    'INTER_AREA': "Area",
    'INTER_LANCZOS4': "Lanczos4"
}
def write_to_csv(data, filename):
    with open(filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(data)

def get_image_size_in_kb(image_path):
    try:
        with Image.open(image_path) as img:
            size_in_bytes = os.path.getsize(image_path)
            size_in_kb = size_in_bytes / 1024
            return round(size_in_kb, 2)
    except Exception as e:
        print(f"Error: {e}")
        return None
    

# rows = []
# rows.append(["resolution", "original"] + [ip_methods_name_mapper[ip_method] + "_0.7" for ip_method in ip_methods_name_mapper])
# for resolution in resolutions:
#     row = []
#     row.append(resolution)
#     row.append(get_image_size_in_kb(original_image_base_path + "/" + resolution + "/1/0.bmp"))
#     for ip_method in ip_methods_name_mapper:
#         row.append(get_image_size_in_kb(compressed_image_base_path + "/" + ip_method + "/" + str(scaling_factor) + "/" + resolution + "/1/0.bmp"))
#     rows.append(row)
# write_to_csv(rows, "image_size_cam1.csv")

print(len(resolutions))

