import sys
import subprocess
try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError: 
    import fake_gpio as GPIO
from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO, emit
import threading
import os
import json
import motor_control
from pathlib import Path

app = Flask(__name__)
socketio = SocketIO(app)
process = None
output_thread = None
motor_thread = None
motor_stop_event = None
script_running = False

BASE_DIR = Path(__file__).resolve().parent
with open(BASE_DIR / 'pins.json', 'r') as file:
    data = json.load(file)

A1 = data["A1"]
A2 = data["A2"]
A3 = data["A3"]
A4 = data["A4"]

B1 = data["B1"]
B2 = data["B2"]
B3 = data["B3"]
B4 = data["B4"]

C1 = data["C1"]
C2 = data["C2"]
C3 = data["C3"]
C4 = data["C4"]

D1 = data["D1"]
D2 = data["D2"]
D3 = data["D3"]
D4 = data["D4"]


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  

    # setup A
    setup_motor(A1, A2, A3, A4)

    # setup B
    setup_motor(B1, B2, B3, B4)

    # setup C
    setup_motor(C1, C2, C3, C4)

    # setup D
    setup_motor(D1, D2, D3, D4)

def setup_motor(*pins):
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)

def stream_output(process):
    for line in process.stdout:
        socketio.emit('script_output', {'output': line.strip()})
    for line in process.stderr:
        socketio.emit('script_output', {'error': line.strip()})

def set_running_script(value):
    global script_running
    script_running = value

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pins.json')
def pins_json():
    return send_file('pins.json')

@app.route('/presets.json')
def presets_json():
    return send_file('presets.json')

@app.route('/settings')
def settings_page():
    return render_template('settings.html')

@app.route('/update_presets', methods=['POST'])
def update_presets_route():
    data = request.get_json(force=True)
    with open('presets.json', 'w') as f:
        json.dump(data, f, indent=2)
    return jsonify({'status': 'success'})


@app.route('/update_pins', methods=['POST'])
def update_pins_route():
    data = request.get_json(force=True)
    with open('pins.json', 'w') as f:
        json.dump(data, f, indent=2)
    global A1, A2, A3, A4, B1, B2, B3, B4, C1, C2, C3, C4, D1, D2, D3, D4
    A1 = data['A1']; A2 = data['A2']; A3 = data['A3']; A4 = data['A4']
    B1 = data['B1']; B2 = data['B2']; B3 = data['B3']; B4 = data['B4']
    C1 = data['C1']; C2 = data['C2']; C3 = data['C3']; C4 = data['C4']
    D1 = data['D1']; D2 = data['D2']; D3 = data['D3']; D4 = data['D4']
    return jsonify({'status': 'success'})

@socketio.on('start_motor')
def start_motor(data):
    global motor_thread, motor_stop_event, script_running
    if motor_thread and motor_thread.is_alive():
        emit('script_output', {'error': 'A script is already running.'})
        return
    
    motor_id = data['motor_id']
    direction = data['direction']

    with open('speed.txt', 'r') as file:
        time = file.read()
        time = float(time)

    motor_stop_event = threading.Event()
    motor_thread = threading.Thread(
        target=motor_control.run_motor,
        args=(motor_id, time, direction, motor_stop_event)
    )

    motor_thread.start()
    script_running = True
    emit('script_output', {
        'output': f'Motor {motor_id} started moving {direction}.'
    })

    

@socketio.on('start_script')
def start_script(data):
    global process, output_thread, script_running
    if process:
        process.terminate()
        process.wait()
        output_thread.join()
        process = None
        emit('script_output', {'error': 'A script is already running.'})
        return

    script_name = data['script_name']
    BASE_DIR = Path(__file__).resolve().parent
    preset_path = os.path.join(BASE_DIR, 'presets')
    script_path = os.path.join(preset_path, script_name)
 
    process = subprocess.Popen([sys.executable, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output_thread = threading.Thread(target=stream_output, args=(process,))
    output_thread.start()
    #script_running = True
    emit('script_output', {'output': 'Script started...'})

@socketio.on('stop_script')
def stop_script():
    global process, output_thread, motor_thread, motor_stop_event
    if process:
        process.terminate()
        process.wait()
        output_thread.join()
        emit('script_output', {'output': 'Script terminated.'})
        
        process = None
    elif motor_thread:
        motor_stop_event.set()
        motor_thread.join()
        emit('script_output', {'output': 'Motor stopped.'})

        motor_thread = None
        motor_stop_event = None
        

@socketio.on('set_speed')
def set_speed(data):
    file_path = 'speed.txt'

    try:

        if not isinstance(data, dict):
            raise ValueError("Expected data to be a dictionary")
        
        key = 'speed_value'  
        if key not in data:
            raise KeyError(f"Key '{key}' not found in data")
        
        value_str = data[key] 
        value = float(value_str) 
    
        
        with open(file_path, 'w') as file:
            value = 0.003 - (value * 0.000024)
            file.write(str(value)) 
    
    except KeyError as e:
        print(f"Error: {e}")
        raise
    
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")
        raise




def main():
    
    gpio_lock = threading.Lock()
    file_path = 'speed.txt'
    with open(file_path, 'w') as file:
            value = 0.003 - (50 * 0.000024)
            file.write(str(value)) 
    setup()
    socketio.run(app, host='0.0.0.0', port=5000)
