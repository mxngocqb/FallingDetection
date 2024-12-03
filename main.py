import json
import os
import queue
from flask import Flask, render_template, Response, request, jsonify
from esp32cam_streamer import ESP32CamStreamer
from video import VideoProcessor, VideoStreamer, FileVideoStreamer

app = Flask(__name__, template_folder='templates')

# File paths for saving data
IP_FILE_PATH = 'ip_addresses.json'
FILE_STREAMS_PATH = 'file_streams.json'

# Global variables
frame_queues = {
    1: queue.Queue(maxsize=10),
    2: queue.Queue(maxsize=10),
    3: queue.Queue(maxsize=10),
    4: queue.Queue(maxsize=10) 
}

ip_addresses = {}
file_streams = {}

# Load data from files if available
def load_data():
    global ip_list, file_list
    if os.path.exists(IP_FILE_PATH):
        with open(IP_FILE_PATH, 'r') as f:
            ip_list = json.load(f)
    else:
        ip_list = {}

    for ip in ip_list:
        ip_addresses[int(ip)] = ip_list[ip]

# Save data to files
def save_data():
    with open(IP_FILE_PATH, 'w') as f:
        json.dump(ip_addresses, f)
    

# Initialize VideoProcessors for each camera
video_processors = {
    camera_id: VideoProcessor('ok.pt', frame_queues[camera_id])
    for camera_id in frame_queues
}

video_streamers_file = {
    camera_id: FileVideoStreamer(frame_queues[camera_id])
    for camera_id in frame_queues
}

@app.route('/home')
def index():
    load_data()
    print(ip_addresses)
    return render_template('index.html')

@app.route('/set_ip', methods=['POST'])
def set_ip():
    data = request.get_json()
    camera_id = data.get('camera_id')
    ip_address = data.get('ip')
    ip_addresses[camera_id] = ip_address
    print(ip_addresses)
    save_data()  # Save updated IP addresses to file
    print(f"Received IP address: {ip_address} for camera ID: {camera_id}")
    return jsonify({'message': 'IP address set successfully'}), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    camera_id = int(request.form.get('camera_id'))  
    if camera_id not in frame_queues:
        return jsonify({'error': 'Invalid camera ID'}), 400

    filename = file.filename
    file_path = os.path.join('uploads', filename)
    file.save(file_path)

    video_processors[camera_id].start_processing(file_path, camera_id)
    file_streams[camera_id] = file_path  # Store the file path for the camera ID
    save_data()  # Save updated file streams to file

    return jsonify({'message': 'File uploaded successfully'}), 200

@app.route('/video_feed/<int:camera_id>')
def video_feed(camera_id):

    if camera_id in ip_addresses:
        
        ip_address = ip_addresses[camera_id]
        print(f"Streaming from IP address: {ip_address} for camera ID: {camera_id}")
        esp32_cam = ESP32CamStreamer(f"http://{ip_address}/")
        video_processor = video_processors[camera_id]
        streamer = VideoStreamer(esp32_cam, video_processor)
        return Response(streamer.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    elif camera_id in file_streams:

        print(f"Streaming from file for camera ID: {camera_id}")
        streamer = video_streamers_file[camera_id]
        return Response(streamer.get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    else:
        print(f"Camera ID {camera_id} not found")
        return jsonify({'error': 'Camera ID not found'}), 404

if __name__ == "__main__":
    # Load data before starting the app
    load_data()
    
    os.makedirs('uploads', exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
