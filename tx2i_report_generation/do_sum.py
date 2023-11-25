import json


resolutions = {
    "cam1": ['160x90', '160x100', '160x120', '240x180', '320x180', '320x200', '320x240', '480x270', '480x300', '480x360', '640x360', '640x400', '640x480', '800x450', '800x500', '800x600', '1024x576', '1024x640', '1024x768', '1280x720', '1280x800', '1280x960', '1440x900', '1440x1080', '1920x1080'],
    "cam2": ['160x90', '160x100', '160x120', '240x180', '320x180', '320x200', '320x240', '480x270', '480x300', '480x360', '640x360', '640x400', '640x480', '800x450', '800x500', '800x600', '1024x576', '1024x640', '1024x768', '1280x720', '1280x800', '1280x960', '1440x900', '1440x1080', '1920x1080'],
    "cam3": ['160x90', '160x120', '176x144', '240x180', '320x180', '320x240', '480x270', '480x360', '640x360', '640x480', '800x450', '800x600', '1024x640', '1024x768', '1280x720', '1280x800', '1280x960'],
    "cam4": ['streamid_1/quality_1', 'streamid_1/quality_2', 'streamid_1/quality_3', 'streamid_1/quality_4', 'streamid_1/quality_5', 'streamid_0/quality_1', 'streamid_0/quality_2', 'streamid_0/quality_3', 'streamid_0/quality_4', 'streamid_0/quality_5']
}

def load_json(json_path):
    with open(json_path, 'r') as file:
        loaded_data = json.load(file)
        return loaded_data

def save_to_json(new_json_path, data):
    with open(new_json_path, 'w') as file:
        json.dump(data, file)
        

def do_sum(exp_id):
    transfer_data = load_json("/home/rouf-linux/edge-computing/tx2i_report_generation/raw_data/transfer_time/" + str(exp_id) + ".json")
    detection_data = load_json("/home/rouf-linux/edge-computing/tx2i_report_generation/raw_data/detection_time/" + str(exp_id) + ".json")
    transfer_data = transfer_data["original"]
    sum_data = {}
    for cam in resolutions:
        for resolution in resolutions[cam]:
            key = cam + "/" + resolution
            sum_data[key] = detection_data[key] + transfer_data["original/" + key]["response_time"]
    return sum_data

for i in range(1, 11):
    sum_data = do_sum(i)
    save_to_json("/home/rouf-linux/edge-computing/tx2i_report_generation/raw_data/detection_transfer_sum_time/" + str(i) + ".json", sum_data)
