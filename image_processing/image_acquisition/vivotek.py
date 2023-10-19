import os
import requests
import csv
from datetime import datetime
import time
from requests.auth import HTTPDigestAuth
from PIL import Image

base_folder = "/home/rouf-linux/Documents/codes/image_acquisition/results"

# Function to create folders based on the specified structure
def create_folders(base_folder, stream_ids, quality_ids, max_images):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    main_folder = os.path.join(base_folder, f"vivotek_{timestamp}")
    os.makedirs(main_folder)
    for stream_id in stream_ids:
        stream_folder = os.path.join(main_folder, f"streamid_{stream_id}")
        os.makedirs(stream_folder)
        for quality_id in quality_ids:
            quality_folder = os.path.join(stream_folder, f"quality_{quality_id}")
            os.makedirs(quality_folder)
            # Create CSV file to record request times
            csv_path = os.path.join(quality_folder, f"request_times_{quality_id}.csv")
            with open(csv_path, "w", newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(["image_id", "image_path", "resolution", "size_kb", "request_time_ms"])

            image_id = 0
            for image_count in [2**i for i in range(max_images + 1)]:
                image_folder = os.path.join(quality_folder, str(image_count))
                os.makedirs(image_folder)

                # Download images and save to the folder, record request times in CSV
                download_images(stream_id, quality_id, image_count, image_folder, csv_path, image_id)
                image_id = image_id + image_count

def download_images(stream_id, quality_id, image_count, folder_path, csv_path, image_id):
    base_url = "http://192.168.1.190/cgi-bin/viewer/video.jpg"
    username = "root"
    password = "admin001"

    with open(csv_path, "a", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)

        for i in range(image_count):
            params = {"quality": quality_id, "streamid": stream_id}
            auth = HTTPDigestAuth(username, password)
            start_time = datetime.now()

            response = requests.get(base_url, params=params, auth=auth)

            end_time = datetime.now()
            request_time_ms = (end_time - start_time).total_seconds() * 1000

            if response.status_code == 200:
                image_path = os.path.join(folder_path, f"{image_id}.jpeg")
                with open(image_path, "wb") as f:
                    f.write(response.content)
                    print(stream_id, quality_id, image_count, i, "written")

                # Calculate image resolution
                image = Image.open(image_path)
                resolution = image.size

                # Calculate image size in KB
                size_kb = os.path.getsize(image_path) / 1024.0

                # Write image information to CSV
                
                image_rel_path = os.path.relpath(image_path, base_folder)
                csv_writer.writerow([image_id, image_rel_path, resolution, size_kb, request_time_ms])
                image_id = image_id + 1
            else:
                print(f"Failed to download image {i} for stream {stream_id}, quality {quality_id}")

            # Introduce a 1-second delay between API calls
            time.sleep(0.2)

def main():
    stream_ids = [0, 1]
    quality_ids = [1, 2, 3, 4, 5]
    max_images = 6

    create_folders(base_folder, stream_ids, quality_ids, max_images)

if __name__ == "__main__":
    main()
