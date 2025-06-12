try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:  # pragma: no cover - hardware dependency
    import fake_gpio as GPIO
from time import sleep
import json
import threading
from pathlib import Path
import server

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / 'pins.json', 'r') as f:
    data = json.load(f)

MOTORS = {
    'A': [data['A1'], data['A2'], data['A3'], data['A4']],
    'B': [data['B1'], data['B2'], data['B3'], data['B4']],
    'C': [data['C1'], data['C2'], data['C3'], data['C4']],
    'D': [data['D1'], data['D2'], data['D3'], data['D4']],
}

FORWARD_SEQUENCE = [
    [3],
    [3, 2],
    [2],
    [1, 2],
    [1],
    [0, 1],
    [0],
    [0, 3],
]
BACKWARD_SEQUENCE = list(reversed(FORWARD_SEQUENCE))

def setup_motor(pins):
    GPIO.setmode(GPIO.BCM)
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)

def step(pins, pattern, delay):
    for i in range(4):
        GPIO.output(pins[i], i in pattern)
    sleep(delay)

def run_motor_steps(motor_id, steps, delay, direction):
    pins = MOTORS[motor_id]
    setup_motor(pins)
    sequence = FORWARD_SEQUENCE if direction == 'forward' else BACKWARD_SEQUENCE
    for _ in range(steps):
        for pattern in sequence:
            step(pins, pattern, delay)
    for pin in pins:
        GPIO.output(pin, False)

def run_preset(name):
    with open(BASE_DIR / 'presets.json', 'r') as f:
        presets = json.load(f)
    cfg = presets.get(name)
    if not cfg:
        raise ValueError(f'Preset {name} not found')
    total_time = cfg.get('time', 15)
    threads = []
    for motor in ['A', 'B', 'C', 'D']:
        mc = cfg.get(motor, {})
        steps = mc.get('steps', 0)
        direction = mc.get('direction', 'forward')
        if steps:
            delay = total_time / steps / 8
            t = threading.Thread(target=run_motor_steps, args=(motor, steps, delay, direction))
            threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    GPIO.cleanup()
    server.set_running_script(False)
    