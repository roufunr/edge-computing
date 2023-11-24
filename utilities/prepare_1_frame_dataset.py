import os
import shutil

cameras = {
    "cam1": "p3245_axis_20231010_020941",
    "cam2": "p3265_axis_20231009_223413",
    "cam3": "p3364_axis_20231009_214248",
    "cam4": "vivotek_20231009_201139"
}

resolutions = {
    "cam1": ['160x90', '160x100', '160x120', '240x180', '320x180', '320x200', '320x240', '480x270', '480x300', '480x360', '640x360', '640x400', '640x480', '800x450', '800x500', '800x600', '1024x576', '1024x640', '1024x768', '1280x720', '1280x800', '1280x960', '1440x900', '1440x1080', '1920x1080'],
    "cam2": ['160x90', '160x100', '160x120', '240x180', '320x180', '320x200', '320x240', '480x270', '480x300', '480x360', '640x360', '640x400', '640x480', '800x450', '800x500', '800x600', '1024x576', '1024x640', '1024x768', '1280x720', '1280x800', '1280x960', '1440x900', '1440x1080', '1920x1080'],
    "cam3": ['160x90', '160x120', '176x144', '240x180', '320x180', '320x240', '480x270', '480x360', '640x360', '640x480', '800x450', '800x600', '1024x640', '1024x768', '1280x720', '1280x800', '1280x960'],
    "cam4": ['streamid_1/quality_1', 'streamid_1/quality_2', 'streamid_1/quality_3', 'streamid_1/quality_4', 'streamid_1/quality_5', 'streamid_0/quality_1', 'streamid_0/quality_2', 'streamid_0/quality_3', 'streamid_0/quality_4', 'streamid_0/quality_5']
}

source_data_path = "/home/rouf-linux/data"
destination_data_path = "/home/rouf-linux/single-frame-data"


for cam in cameras:
    camera_name = cameras[cam]
    for resolution in resolutions[cam]:
        dest_path = destination_data_path + "/" + cam + "/" + resolution + "/"
        os.makedirs(dest_path, exist_ok=True)
        source_file_path = source_data_path + "/" + camera_name + "/" + resolution + "/1/"
        if cam == "cam4":
            source_file_path += "0.jpeg"
            dest_path += "0.jpeg"
        else: 
            source_file_path += "0.bmp"
            dest_path += "0.bmp"
            
        shutil.copy2(source_file_path, dest_path)