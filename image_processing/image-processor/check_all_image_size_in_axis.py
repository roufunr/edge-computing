import os
import requests
from requests.auth import HTTPDigestAuth

# API endpoint and authentication details
url = "http://134.197.94.53/axis-cgi/bitmap/image.bmp"
auth = HTTPDigestAuth('root', 'pass')

# Supported resolutions
resolutions = [
    "1920x1080", "1440x1080", "1440x900", "1280x960", "1280x800",
    "1280x720", "1024x768", "1024x640", "1024x576", "800x600",
    "800x500", "800x450", "640x480", "640x400", "640x360", 
    "480x360", "480x300", "480x270", "320x240", "320x200",
    "320x180", "240x180", "160x120", "160x100", "160x90"
]

# Create a directory to save the results
if not os.path.exists('results'):
    os.makedirs('results')

# Loop through each resolution and capture/save the image
for resolution in resolutions:
    params = {
        'resolution': resolution,
        'camera': 1
    }

    response = requests.get(url, auth=auth, params=params)
    
    if response.status_code == 200:
        image_filename = f'results/captured_{resolution}.bmp'
        with open(image_filename, 'wb') as image_file:
            image_file.write(response.content)
        image_size_kb = len(response.content) / 1024
        print(f'{resolution} - Image Size: {image_size_kb:.2f} KB')
    else:
        print(f'{resolution} - Request failed with status code: {response.status_code}')

print('Capture process complete.')
