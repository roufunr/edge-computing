import pandas as pd

raw_results_base_path = "/Users/abdurrouf/edge-computing/image_transfer/report_generation/raw_results"
parts = ["compression", "decompression", "transfer"]
transfer_image_type = ["original", "compressed"]
transfer_time_type = ["transfer_time", "disk_write_time", "response_time"]
resolutions = ['160x90', '160x100', '160x120', '320x180', '320x200', '320x240', '480x270', '480x300', '480x360', '640x360', '640x400', '640x480', '800x450', '800x500', '800x600', '1024x576', '1024x640', '1024x768', '1280x720', '1280x800', '1280x960', '1440x900', '1440x1080', '1920x1080']
frames = [1, 2, 4, 8, 16, 32]
total_experiment = 10
scaling_factors = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
ip_methods = ['INTER_NEAREST', 'INTER_LINEAR', 'INTER_CUBIC', 'INTER_AREA', 'INTER_LANCZOS4']
ip_methods_name_mapper = {
    'INTER_NEAREST': "Nearest",
    'INTER_LINEAR': "Linear",
    'INTER_CUBIC': "Cubic",
    'INTER_AREA': "Area",
    'INTER_LANCZOS4': "Lanczos4"
}


def merge_csv_files_with_empty_column(csv_file_paths, output_file_path):
    try:
        merged_data = pd.DataFrame()

        for i, file_path in enumerate(csv_file_paths):
            df = pd.read_csv(file_path)

            if not merged_data.empty:
                # Add an empty column before merging, except for the first file
                merged_data[''] = ''
                merged_data = pd.concat([merged_data, df], axis=1)
            else:
                merged_data = df

        merged_data.to_csv(output_file_path, index=False)
        print(f"CSV files have been successfully merged with empty columns and saved to '{output_file_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

# transfer
csv_list = []
for ip_method in ip_methods:
    for scaling_factor in scaling_factors:
        csv_list.append("/Users/abdurrouf/edge-computing/image_transfer/report_generation/csv/transfer/compressed" + "/" + ip_method + "/" + str(scaling_factor) + ".csv")
output_csv_path = "/Users/abdurrouf/edge-computing/image_transfer/report_generation/deliverable_csv" + "/" + "compressed_image_transfer.csv"
merge_csv_files_with_empty_column(csv_list, output_csv_path)

# compression
csv_list = []
for ip_method in ip_methods:
    for scaling_factor in scaling_factors:
        csv_list.append("/Users/abdurrouf/edge-computing/image_transfer/report_generation/csv/compression" + "/" + ip_method + "/" + str(scaling_factor) + ".csv")
output_csv_path = "/Users/abdurrouf/edge-computing/image_transfer/report_generation/deliverable_csv" + "/" + "image_compression_time.csv"
merge_csv_files_with_empty_column(csv_list, output_csv_path)

# decompression
csv_list = []
for ip_method in ip_methods:
    for scaling_factor in scaling_factors:
        csv_list.append("/Users/abdurrouf/edge-computing/image_transfer/report_generation/csv/decompression" + "/" + ip_method + "/" + str(scaling_factor) + ".csv")
output_csv_path = "/Users/abdurrouf/edge-computing/image_transfer/report_generation/deliverable_csv" + "/" + "image_decompression_time.csv"
merge_csv_files_with_empty_column(csv_list, output_csv_path)
