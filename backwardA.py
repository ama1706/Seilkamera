import RPi.GPIO as GPIO
from time import sleep
import threading as th

A = 24
B = 25
C = 4
D = 17

with open('speed.txt', 'r') as file:
    time = file.read()
    time = float(time)

def setup_motor(*pins):
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)



def Step1(D, time):
    GPIO.output(D, True)
    sleep(time)
    GPIO.output(D, False)

def Step2(D, C, time):
    GPIO.output(D, True)
    GPIO.output(C, True)
    sleep(time)
    GPIO.output(D, False)
    GPIO.output(C, False)

def Step3(C, time):
    GPIO.output(C, True)
    sleep(time)
    GPIO.output(C, False)

def Step4(B, C, time):
    GPIO.output(B, True)
    GPIO.output(C, True)
    sleep(time)
    GPIO.output(B, False)
    GPIO.output(C, False)

def Step5(B, time):
    GPIO.output(B, True)
    sleep(time)
    GPIO.output(B, False)

def Step6(A, B, time):
    GPIO.output(A, True)
    GPIO.output(B, True)
    sleep(time)
    GPIO.output(A, False)
    GPIO.output(B, False)

def Step7(A, time):
    GPIO.output(A, True)
    sleep(time)
    GPIO.output(A, False)

def Step8(A, D, time):
    GPIO.output(D, True)
    GPIO.output(A, True)
    sleep(time)
    GPIO.output(D, False)
    GPIO.output(A, False)


gpio_lock = th.Lock()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
setup_motor(A, B, C, D)

try: 
    while True:
        Step8(A, D, time)
        Step7(A, time)
        Step6(A, B, time)
        Step5(B, time)
        Step4(B, C, time)
        Step3(C, time)
        Step2(D, C, time)
        Step1(D, time)
finally:
        GPIO.cleanup()