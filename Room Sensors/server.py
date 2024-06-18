from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import threading
import time
import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins for WebSocket connections

# Dictionary to store data and last seen time from each ESP32
esp_data = {}
offline_threshold = 7  # Threshold in seconds to consider an ESP32 offline
server_start_time = time.time()  # Record the server start time

# Function to check and remove offline ESP32s
def check_offline():
    global esp_data
    while True:
        current_time = time.time()
        offline_ips = [ip for ip, data in esp_data.items() if (current_time - data['last_seen']) > offline_threshold]
        for ip in offline_ips:
            del esp_data[ip]
            print(f"ESP32 at {ip} has gone offline and removed from data.")
        time.sleep(offline_threshold)  # Check every 'offline_threshold' seconds

# Start the thread for checking offline ESP32s
offline_check_thread = threading.Thread(target=check_offline)
offline_check_thread.start()

@app.route('/update', methods=['POST'])
def update_data():
    data = request.json
    ip = request.remote_addr
    esp_data[ip] = {
        'temperature': data.get('temperature'),
        'humidity': data.get('humidity'),
        'last_seen': time.time()
    }
    # Emit the data to all connected clients
    socketio.emit('update', {'ip': ip, 'temperature': data.get('temperature'), 'humidity': data.get('humidity')})
    print(f"Updated data from {ip}: {esp_data[ip]}")  # Debug statement
    return jsonify(success=True)

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(esp_data)

@app.route('/uptime', methods=['GET'])
def get_uptime():
    uptime_seconds = time.time() - server_start_time
    uptime_str = str(datetime.timedelta(seconds=int(uptime_seconds)))
    return jsonify({'uptime': uptime_str})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
