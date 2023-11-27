import requests
from requests.auth import HTTPDigestAuth
import time
import csv



resolutions = ['160x90', '160x100', '160x120', '240x180', '320x180', '320x200', '320x240', '480x270', '480x300', '480x360', '640x360', '640x400', '640x480', '800x450', '800x500', '800x600', '1024x576', '1024x640', '1024x768', '1280x720', '1280x800', '1280x960', '1440x900', '1440x1080', '1920x1080']
# Specify the number of iterations to test
num_iterations = 10  


def capture_image(res):
    api_url = "http://192.168.1.101/axis-cgi/bitmap/image.bmp?resolution=" + res + "&camera=1"
    auth_credentials = ('root', 'pass')
    response = requests.get(api_url, auth=HTTPDigestAuth(*auth_credentials))
    if response.status_code == 200:
        pass
    else:
        print(f"Error: {response.status_code}")

def find_median(lst):
    sorted_lst = sorted(lst)
    n = len(sorted_lst)

    if n % 2 == 0:
        mid1 = sorted_lst[n // 2 - 1]
        mid2 = sorted_lst[n // 2]
        median = (mid1 + mid2) / 2
    else:
        median = sorted_lst[n // 2]

    return median

def write_to_csv(data, filename):
    with open(filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(data)

def measure_fpm(res):
    fpm_list = []
    print("STARTED ::: " + res)
    for i in range(10):
        start_time = time.time()
        for _ in range(num_iterations):
            capture_image(res)
        end_time = time.time()
        elapsed_time = end_time - start_time
        fpm = (num_iterations / elapsed_time) * 60
        fpm_list.append(fpm)
    median_fpm = round(find_median(fpm_list))
    print("END ::: " + res + " :: fpm " + str(median_fpm))
    return median_fpm

rows = []
for resolution in resolutions:
    row = []
    row.append(resolution)
    fpm = measure_fpm(resolution)
    row.append(fpm)
    rows.append(row)

write_to_csv(rows, "FPM")


