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
from RPLCD.i2c import CharLCD

# ---------------------- Sensor and GPIO Setup ---------------------- #
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28-01202684e4ed')[0]
device_file = device_folder + '/w1_slave'

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Status and control flags
lights_status = False
heater_status = False
pump_status = False
cabinetlights_status = False
float_switch_status = False
heater_on_temp = 24.0
heater_off_temp = 25.0
lights_on_time = 1100
lights_off_time = 2100
xTime = 0

# GPIO pin assignments
lights_relay = 23
heater_relay = 24
pump_relay = 25
cabinetlights_relay = 8
float_switch_pin = 7

GPIO.setup(lights_relay, GPIO.OUT)
GPIO.setup(heater_relay, GPIO.OUT)
GPIO.setup(pump_relay, GPIO.OUT)
GPIO.setup(cabinetlights_relay, GPIO.OUT)
GPIO.setup(float_switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# LCD setup
lcd = CharLCD('PCF8574', address=0x27, port=1, cols=16, rows=2)

# Status indicator
pi1StatusIndicator = "⦿ Online"

# ---------------------- Helper Functions ---------------------- #
def get_system_uptime():
    try:
        output = subprocess.check_output("uptime", shell=True).decode()
        uptime = output.split("up")[1].split(",")[0].strip()
        return uptime
    except Exception as e:
        print("Error:", e)
        return None

def read_temp_raw():
    with open(device_file, 'r') as f:
        return f.readlines()

def read_temp_c():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.5)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        return round(int(float(temp_string) / 1000))

def read_temp_c_decimal():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.5)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        return round(float(temp_string) / 1000, 1)

def get_current_datetime():
    global intTime, xTime
    intTime = datetime.now()
    xTime = int(intTime.strftime("%H%M"))
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_current_time():
    return int(datetime.now().strftime("%H%M"))

def initialize_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(lights_relay, GPIO.OUT)
    GPIO.setup(heater_relay, GPIO.OUT)
    GPIO.setup(pump_relay, GPIO.OUT)
    GPIO.setup(cabinetlights_relay, GPIO.OUT)
    GPIO.setup(float_switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def update_lcd(temp, pump, heater, lights):
    lcd.clear()
    lcd.write_string(f" T:{temp:.1f}c  P:{'ON' if pump else 'OFF'}")
    lcd.crlf()
    lcd.write_string(f" L:{'ON' if lights else 'OFF'}    H:{'ON' if heater else 'OFF'}")


# ---------------------- Flask App ---------------------- #
app = Flask(__name__)
CORS(app)

@app.route('/control/reboot', methods=['POST'])
def control_pi():
    command = request.get_json().get('command')
    if command == 'reboot':
        reboot_raspberry_pi()

def reboot_raspberry_pi():
    try:
        os.system('sudo reboot')
    except Exception as e:
        print("Error:", e)

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

@app.route('/control/cabinetlights', methods=['POST'])
def control_cabinet_lights():
    global cabinetlights_status
    command = request.get_json().get('command')
    if command == 'cabinetlights_on':
        cabinetlights_status = True
        print('working')
        GPIO.output(cabinetlights_relay, GPIO.HIGH)
    elif command == 'cabinetlights_off':
        cabinetlights_status = False
        GPIO.output(cabinetlights_relay, GPIO.LOW)
    return jsonify({'cabinetlights_status': cabinetlights_status})

@app.route('/set/heater/on-temp', methods=['POST'])
def set_heater_on_temp():
    global heater_on_temp
    heater_on_temp = request.get_json().get('heater_on_temp')
    return jsonify({'heater_on_temp': heater_on_temp})

@app.route('/set/heater/off-temp', methods=['POST'])
def set_heater_off_temp():
    global heater_off_temp
    heater_off_temp = request.get_json().get('heater_off_temp')
    return jsonify({'heater_off_temp': heater_off_temp})

@app.route('/set/lights/on-time', methods=['POST'])
def set_lights_on_time():
    global lights_on_time
    lights_on_time = request.get_json().get('lights_on_time')
    return jsonify({'lights_on_time': lights_on_time})

@app.route('/set/lights/off-time', methods=['POST'])
def set_lights_off_time():
    global lights_off_time
    lights_off_time = request.get_json().get('lights_off_time')
    return jsonify({'lights_off_time': lights_off_time})

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({
        'light_status': lights_status,
        'heater_status': heater_status,
        'pump_status': pump_status,
        'cabinet_lights_status': cabinetlights_status,
        'water_temperature': read_temp_c_decimal(),
        'current_datetime': get_current_datetime(),
        'pi1StatusIndicator': pi1StatusIndicator,
        'heater_on_temp': heater_on_temp,
        'heater_off_temp': heater_off_temp,
        'lights_on_time': lights_on_time,
        'lights_off_time': lights_off_time,
        'int_time': xTime,
        'system_uptime': get_system_uptime()
    })

# ---------------------- Main Loop Thread ---------------------- #
def update_relays_thread():
    global lights_status, heater_status, pump_status, float_switch_status

    while True:
        initialize_gpio()
        heater_on_temp1 = int(heater_on_temp)
        heater_off_temp1 = int(heater_off_temp)
        lights_on_time1 = int(lights_on_time)
        lights_off_time1 = int(lights_off_time)

        try:
            current_time = get_current_time()
            current_temp = read_temp_c()
            print("Current Time:", current_time)
            print("Water Temp:", current_temp)

            # Lights control
            if lights_on_time1 <= current_time < lights_off_time1:
                lights_status = True
                GPIO.output(lights_relay, GPIO.HIGH)
                print("Lights ON")
            else:
                lights_status = False
                GPIO.output(lights_relay, GPIO.LOW)
                print("Lights OFF")

            # Heater control
            if heater_on_temp1 >= current_temp or heater_off_temp1 > current_temp:
                heater_status = True
                GPIO.output(heater_relay, GPIO.HIGH)
                print("Heater ON")
            else:
                heater_status = False
                GPIO.output(heater_relay, GPIO.LOW)
                print("Heater OFF")

            # Pump via float switch
            float_switch_state = GPIO.input(float_switch_pin)
            float_switch_status = float_switch_state == GPIO.HIGH

            if float_switch_status:
                GPIO.output(pump_relay, GPIO.HIGH)
                pump_status = True
                print("Pump ON (float switch triggered)")
            else:
                GPIO.output(pump_relay, GPIO.LOW)
                pump_status = False
                print("Pump OFF")

            # Update LCD
            update_lcd(read_temp_c_decimal(), pump_status, heater_status, lights_status)

            print("Note: Looping every 10 seconds.")
            time.sleep(3)

        except Exception as e:
            print(f"Error: {e}")
            thread = Thread(target=update_relays_thread)
            thread.start()

# ---------------------- Start Application ---------------------- #
if __name__ == '__main__':
    initialize_gpio()
    thread = Thread(target=update_relays_thread)
    thread.start()
    app.run(host='0.0.0.0', port=5000)
