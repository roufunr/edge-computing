import os
import requests
from datetime import datetime
import time
import csv
from requests.auth import HTTPDigestAuth

ip_camera_model_mapper = {'192.168.1.101': 'p3245_axis', 
                          #'192.168.1.159': 'p3364_axis', 
                          #'192.168.1.144': 'p3265_axis'
}
ip_resolutions_mapper = {
    '192.168.1.101': '1920x1080,1440x1080,1440x900,1280x960,1280x800,1280x720,1024x768,1024x640,1024x576,800x600,800x500,800x450,640x480,640x400,640x360,480x360,480x300,480x270,320x240,320x200,320x180,240x180,160x120,160x100,160x90',
    #'192.168.1.159': '1280x960,1024x768,800x600,640x480,480x360,320x240,240x180,160x120,1280x720,800x450,640x360,480x270,320x180,160x90,1280x800,1024x640,176x144',
    #'192.168.1.144': '1920x1080,1440x1080,1440x900,1280x960,1280x800,1280x720,1024x768,1024x640,1024x576,800x600,800x500,800x450,640x480,640x400,640x360,480x360,480x300,480x270,320x240,320x200,320x180,240x180,160x120,160x100,160x90'
}

result_dir = '/home/rouf-linux/Documents/codes/image_acquisition/results/data'
api_endpoint = 'http://{}/axis-cgi/bitmap/image.bmp?resolution={}&camera=1'
digest_auth = ('root', 'pass')
wait_time = 0.1  # 100 ms

def create_folders(ip, timestamp, resolutions):
    camera_model_folder = os.path.join(result_dir, f'{ip_camera_model_mapper[ip]}_{timestamp}')
    os.makedirs(camera_model_folder)

    for resolution in resolutions.split(','):
        resolution_folder = os.path.join(camera_model_folder, resolution)
        os.makedirs(resolution_folder)

        # Create CSV file for each resolution
        csv_path = os.path.join(resolution_folder, f'request_times_{resolution}.csv')
        with open(csv_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["image_id", "image_path", "resolution", "size_kb", "request_time_ms"])

        for divisor in [1, 2, 4, 8, 16, 32, 64]:
            divisor_folder = os.path.join(resolution_folder, str(divisor))
            os.makedirs(divisor_folder)

def capture_and_save_image(url, auth, save_path, image_id, resolution):
    start_time = time.time()
    response = requests.get(url, auth=auth, stream=True)
    end_time = time.time()

    with open(save_path, 'wb') as img_file:
        for chunk in response.iter_content(chunk_size=128):
            img_file.write(chunk)

    size_kb = os.path.getsize(save_path) / 1024.0
    request_time_ms = (end_time - start_time) * 1000.0

    # Append data to CSV file
    csv_path = os.path.join(os.path.dirname(save_path), f'request_times_{resolution}.csv')
    with open(csv_path, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([image_id, os.path.relpath(save_path, result_dir), resolution, size_kb, request_time_ms])

def run_image_capture(ip):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    resolutions = ip_resolutions_mapper[ip]

    create_folders(ip, timestamp, resolutions)

    for resolution in resolutions.split(','):
        resolution_folder = os.path.join(result_dir, f'{ip_camera_model_mapper[ip]}_{timestamp}', resolution)
        divisor = 1
        image_id = 0

        while divisor <= 64:
            divisor_folder = os.path.join(resolution_folder, str(divisor))

            for i in range(divisor):
                image_path = os.path.join(divisor_folder, f'{image_id}.bmp')
                api_url = api_endpoint.format(ip, resolution, 1)
                capture_and_save_image(api_url, HTTPDigestAuth(*digest_auth), image_path, image_id, resolution)

                print(f"Resolution: {resolution}, Divisor: {divisor}, Image ID: {image_id}")
                image_id += 1

            divisor *= 2
            time.sleep(wait_time)

# Example usage:
for ip_address in ip_camera_model_mapper.keys():
    run_image_capture(ip_address)
