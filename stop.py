import RPi.GPIO as GPIO
from time import sleep
import threading as th


A1 = 24
A2 = 25
A3 = 4
A4 = 17

B1 = 27
B2 = 22
B3 = 10
B4 = 9

C1 = 11
C2 = 5
C3 = 6
C4 = 13

D1 = 19
D2 = 26
D3 = 18
D4 = 23

T1 = 12
T2 = 16
T3 = 20
T4 = 21

def main():
    gpio_lock = th.Lock()
    setup()

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # Set pin numbering mode

    # setup A
    setup_motor(A1, A2, A3, A4)

    # setup B
    setup_motor(B1, B2, B3, B4)

    # setup C
    setup_motor(C1, C2, C3, C4)

    # setup D
    setup_motor(D1, D2, D3, D4)

    # setup T
    setup_motor(T1, T2, T3, T4)

def setup_motor(*pins):
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)

main()
GPIO.cleanup()