import os
import csv

data_path = "/home/ubuntu/data_32"
cameras = {
    'cam1': 'p3245_axis_20231010_020941',
    'cam2': 'p3265_axis_20231009_223413',
    'cam3': 'p3364_axis_20231009_214248',
    'cam4': 'vivotek_20231009_201139'
}
resolutions = {
    'p3245_axis_20231010_020941': ['160x90', '160x100', '160x120', '240x180', '320x180', '320x200', '320x240', '480x270', '480x300', '480x360', '640x360', '640x400', '640x480', '800x450', '800x500', '800x600', '1024x576', '1024x640', '1024x768', '1280x720', '1280x800', '1280x960', '1440x900', '1440x1080', '1920x1080'],
    'p3265_axis_20231009_223413': ['160x90', '160x100', '160x120', '240x180', '320x180', '320x200', '320x240', '480x270', '480x300', '480x360', '640x360', '640x400', '640x480', '800x450', '800x500', '800x600', '1024x576', '1024x640', '1024x768', '1280x720', '1280x800', '1280x960', '1440x900', '1440x1080', '1920x1080'], 
    'p3364_axis_20231009_214248': ['176x144', '160x90', '160x120', '240x180', '320x180', '320x240', '480x270', '480x360', '640x360', '800x450', '800x600', '640x480', '1024x640', '1280x800', '1024x768', '1280x720', '1280x960'],
    'vivotek_20231009_201139': [
        'streamid_1/quality_1', 'streamid_1/quality_2', 'streamid_1/quality_3', 'streamid_1/quality_4', 'streamid_1/quality_5', 
        'streamid_0/quality_1', 'streamid_0/quality_2', 'streamid_0/quality_3', 'streamid_0/quality_4', 'streamid_0/quality_5',
    ]
}

for camera in cameras:
    table = [[camera + ' - resolution', 'kilobytes']]
    for resolution in resolutions[cameras[camera]]:
        image_path = data_path + "/" + cameras[camera] + "/" + resolution + "/1/0."
        if camera == "cam4":
            image_path += "jpeg"
        else:
            image_path += "bmp"
        file_size = round(os.path.getsize(image_path)/1024)
        table.append([resolution, file_size])
    
    with open(camera + ".csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(table)

        

