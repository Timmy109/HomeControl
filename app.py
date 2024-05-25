## Code for Raspberry Pi Zero ##

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from threading import Thread

import RPi.GPIO as GPIO
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


# Initial status and settings
lights_status = False
heater_status = False
heater_on_temp = 24.0  # initial value
heater_off_temp = 25.0  # initial value
lights_on_time = 1100
lights_off_time = 2100
lights_relay = 23 # Set pin for lights relay
heater_relay = 24 # Set pin for heater relay
xTime = 0000 # initial value

GPIO.setup(lights_relay, GPIO.OUT)
GPIO.setup(heater_relay, GPIO.OUT)

# Update site status
site_status = "⦿ Online"

def get_system_uptime():
    try:
        output = subprocess.check_output("uptime", shell=True).decode()
        uptime = output.split("up")[1].split(",")[0].strip()
        return uptime
    except Exception as e:
        print("Error:", e)
        return None

# print("System uptime:", get_system_uptime())


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

# Get the current date and time
def get_current_datetime():
    global intTime
    global xTime
    intTime = datetime.now()
    xTime = int(intTime.strftime("%H%M"))
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Get the current time (Hours & Minutes)
def get_current_time():
    return int(datetime.now().strftime("%H%M"))

# Route to get the current status
@app.route('/status', methods=['GET'])
def get_status():
    global lights_status, heater_status
    return jsonify({
        'light_status': lights_status,
        'heater_status': heater_status,
        'water_temperature': read_temp_c_decimal(),
        'current_datetime': get_current_datetime(),
        'site_status': site_status,
        'heater_on_temp': heater_on_temp,
        'heater_off_temp': heater_off_temp,
        'lights_on_time': lights_on_time,
        'lights_off_time': lights_off_time,
        'int_time': xTime,
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

# Route to control lights
@app.route('/control/lights', methods=['POST'])
def control_lights():
    global lights_status
    command = request.get_json().get('command')

    if command == 'lights_on':
        lights_status = True
        GPIO.output(lights_relay, GPIO.HIGH)
    elif command == 'lights_off':
        lights_status = False
        GPIO.output(lights_relay, GPIO.LOW)

    return jsonify({'light_status': lights_status})

# Route to control heater
@app.route('/control/heater', methods=['POST'])
def control_heater():
    global heater_status
    command = request.get_json().get('command')

    if command == 'heater_on':
        heater_status = True
        GPIO.output(heater_relay, GPIO.HIGH)
    elif command == 'heater_off':
        heater_status = False
        GPIO.output(heater_relay, GPIO.LOW)

    return jsonify({'heater_status': heater_status})

# Route to set heater-on temperature
@app.route('/set/heater/on-temp', methods=['POST'])
def set_heater_on_temp():
    global heater_on_temp
    heater_on_temp = request.get_json().get('heater_on_temp')
    return jsonify({'heater_on_temp': heater_on_temp})

# Route to set heater-off temperature
@app.route('/set/heater/off-temp', methods=['POST'])
def set_heater_off_temp():
   global heater_off_temp
   heater_off_temp = request.get_json().get('heater_off_temp')
   return jsonify({'heater_off_temp': heater_off_temp})

# Route to set lights-on temperature
@app.route('/set/lights/on-time', methods=['POST'])
def set_lights_on_time():
    global lights_on_time
    lights_on_time = request.get_json().get('lights_on_time')
    return jsonify({'lights_on_time': lights_on_time})\

# Route to set lights-off temperature
@app.route('/set/lights/off-time', methods=['POST'])
def set_lights_off_time():
    global lights_off_time
    lights_off_time = request.get_json().get('lights_off_time')
    return jsonify({'lights_off_time': lights_off_time})

def initialize_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(lights_relay, GPIO.OUT)
    GPIO.setup(heater_relay, GPIO.OUT)

def update_relays_thread():
    global lights_status, heater_status, waterTemp
    while True:
        initialize_gpio()
        heater_on_temp1 = int(heater_on_temp)
        heater_off_temp1 = int(heater_off_temp)
        lights_on_time1 = int(lights_on_time)
        lights_off_time1 = int(lights_off_time)
        print(read_temp_c())

        try:
            print(get_current_time())
            if lights_on_time1 <= get_current_time() and lights_off_time1 > get_current_time():
                lights_status = True
                GPIO.output(lights_relay, GPIO.HIGH)
                print("lights on")
            else:
                lights_status = False
                GPIO.output(lights_relay, GPIO.LOW)
                print("lights off")

            if heater_on_temp1 >= read_temp_c() or heater_off_temp1 > read_temp_c():
                heater_status = True
                GPIO.output(heater_relay, GPIO.HIGH)
                print("heater on")
            else:
                heater_status = False
                GPIO.output(heater_relay, GPIO.LOW)
                print("heater off")

            print("Note: Looping every 60 seconds.")

            time.sleep(60)  # Adjust sleep time as needed - in seconds.

        except Exception as e:
            print(f"Error: {e}")
            thread = Thread(target=update_relays_thread)
            thread.start()
    return

if __name__ == '__main__':

    initialize_gpio()
    thread = Thread(target=update_relays_thread)
    thread.start()
    app.run(host='0.0.0.0', port=5000)
