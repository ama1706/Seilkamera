try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:  # pragma: no cover - hardware dependency
    import fake_gpio as GPIO
from time import sleep
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
with open(BASE_DIR / 'pins.json', 'r') as file:
    data = json.load(file)

A = [data["A1"], data["A2"], data["A3"], data["A4"]]
B = [data["B1"], data["B2"], data["B3"], data["B4"]]
C = [data["C1"], data["C2"], data["C3"], data["C4"]]
D = [data["D1"], data["D2"], data["D3"], data["D4"]]

MOTORS = {
    "A": A,
    "B": B,
    "C": C,
    "D": D
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
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)

def step(pins, pattern, delay):
    for i in range(4):
        GPIO.output(pins[i], i in pattern)
    sleep(delay)

def run_motor(motor_id, delay, direction, stop_event=None):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    pins = MOTORS[motor_id]
    setup_motor(pins)
    sequence = FORWARD_SEQUENCE if direction == "forward" else BACKWARD_SEQUENCE
    try:
        while not (stop_event and stop_event.is_set()):
            for pattern in sequence:
                if stop_event and stop_event.is_set():
                    break
                step(pins, pattern, delay)
    finally:
        GPIO.cleanup()