from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/sensor', methods=['GET'])
def sensor_data():
    # Replace these dummy values with your actual sensor data
    temperature = 25.5
    humidity = 60.0
    return jsonify({'temperature': temperature, 'humidity': humidity})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
