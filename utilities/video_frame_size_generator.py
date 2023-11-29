import os
from xml.etree import ElementTree as ET
from datetime import datetime
import subprocess
import csv
import cv2

root_path = "/home/rouf-linux/Videos/cam1_videos"
frame_path = "/home/rouf-linux/Videos/frames"
frame_rate = 30

def getUnixTime(timestamp_str):
    # timestamp_str = "2023-11-28T18:04:57.771859Z"
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    unix_time = (int(timestamp.timestamp() * 1000 * 1000 * 1000))/(1000 * 1000 * 1000)
    return unix_time

def fileContent(file_path):
    try:
        with open(file_path, 'r') as file:
            file_contents = file.read()
            return file_contents
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"Error: {e}")
    
def write_to_csv(data, filename):
    with open(filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(data)

def getXMLInfo(xml_data_str):
    root = ET.fromstring(xml_data_str)
    width = int(root.find(".//Width").text)
    height = int(root.find(".//Height").text)
    start_time = getUnixTime(root.find(".//StartTime").text)
    end_time = getUnixTime(root.find(".//StopTime").text)
    elapsed_time = end_time - start_time
    return elapsed_time, width, height


def generate_frame(video_path, res):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Frames per Second (fps): {fps}")
    print(f"Frame Size: {frame_size}")
    print(f"Total Frames: {total_frames}")
    for frame_num in range(total_frames):
        ret, frame = cap.read()
        if ret:
            # Save the frame (you can also perform any other processing here)
            frame_dir = frame_path + "/" + res
            os.makedirs(frame_dir, exist_ok=True)
            frame_filename = f'{frame_num + 1}.jpg'
            cv2.imwrite(frame_dir + "/" + frame_filename, frame)
    cap.release()
    print("Frames extracted successfully for video: " + video_path)



videos = [d for d in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, d))]

record_data = []
rows = []
for video in videos:
    recording_xml_path = root_path+ "/" + video + "/recording.xml"
    record_data = getXMLInfo(fileContent(recording_xml_path))
    mkv_files = [file for file in os.listdir(root_path+ "/" + video + "/20231128_10") if file.endswith(".mkv")]
    mkv_file_path = root_path+ "/" + video + "/20231128_10/" + mkv_files[0]
    mkv_file_size = os.path.getsize(mkv_file_path)
    frame_size = mkv_file_size / (frame_rate * record_data[0])
    resolution = str(record_data[1]) + "x" + str(record_data[2])
    rows.append([resolution, frame_size])

    # generate frame
    generate_frame(mkv_file_path, res=resolution)


sorted_data = sorted(rows, key=lambda x: eval(x[0].replace('x', '*')))

write_to_csv(sorted_data, "video_frame_size.csv")



