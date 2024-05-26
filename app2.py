## Code for Gold fish tank ##

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from threading import Thread

# import RPi.GPIO as GPIO
import time
import os
import glob
import subprocess

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28-3c2f0457b76a')[0]
device_file = device_folder + '/w1_slave'

GPIO.setmode(GPIO.BCM)
app = Flask(__name__)
CORS(app)

# Update site status
pi2StatusIndicator = "⦿ Online"

def get_system_uptime():
    try:
        output = subprocess.check_output("uptime", shell=True).decode()
        uptime = output.split("up")[1].split(",")[0].strip()
        return uptime
    except Exception as e:
        print("Error:", e)
        return None

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

#CELSIUS CALCULATION
def read_temp_c():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.5)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        x = float(temp_string)
        y = round(int(float(temp_string) / 1000)) #)
        return y

#CELSIUS CALCULATION WITH DECIMAL
def read_temp_c_decimal():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.5)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        x = float(temp_string)
        y = round(float(temp_string) / 1000,1)
        return y


# Route to get the current status
@app.route('/status', methods=['GET'])
def get_status():
    global lights_status, heater_status
    return jsonify({
        'water_temperature_goldfish': read_temp_c_decimal(),
        'pi2StatusIndicator': pi2StatusIndicator,
        'system_uptime': get_system_uptime()
        })

# Route to reboot pi
@app.route('/control/reboot', methods=['POST'])
def control_pi():
    command = request.get_json().get('command')

    if command == 'reboot':
        reboot_raspberry_pi()

def reboot_raspberry_pi():
    try:
        # Run the 'sudo reboot' command to reboot the Raspberry Pi
        os.system('sudo reboot')
    except Exception as e:
        # If an error occurs, handle it here
        print("Error:", e)

def initialize_gpio():
    GPIO.setmode(GPIO.BCM)

if __name__ == '__main__':

    initialize_gpio()
    app.run(host='0.0.0.0', port=5000)