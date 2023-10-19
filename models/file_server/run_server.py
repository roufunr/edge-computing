from flask import Flask, request, jsonify
import os
from time import time
from datetime import datetime  # Import datetime module

app = Flask(__name__)

# Specify the upload directory
upload_path = "./images"

# Define allowed extensions for images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    transfer_end_time = time() * 1000
    if 'images' not in request.files or 'path' not in request.form:
        return jsonify({'error': 'No file part or path'}), 400

    files = request.files.getlist('images')
    images_path = request.form['path']  # Change from request.path to request.form['path']

    os.makedirs(upload_path + images_path, exist_ok=True)

    disk_write_start_time = time() * 1000
    for file in files:
        exact_file_save_path = upload_path + images_path + file.filename  # Use os.path.join
        file.save(exact_file_save_path)
    disk_write_end_time = time() * 1000
    transfer_time = transfer_end_time - float(request.form['transfer_start_time'])  # Corrected request.form usage
    disk_write_time = disk_write_end_time - disk_write_start_time

    return jsonify({'transfer_time': transfer_time, 'disk_write_time': disk_write_time}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
