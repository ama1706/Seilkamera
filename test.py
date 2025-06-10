import RPi.GPIO as GPIO
from time import sleep
import threading as th

T1 = 12
T2 = 16
T3 = 20
T4 = 21

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
setup_motor(T1, T2, T3, T4)
time = 0.001

try: 
    while True:
        Step1(T4, time)
        Step2(T4, T3, time)
        Step3(T3, time)
        Step4(T2, T3, time)
        Step5(T2, time)
        Step6(T1, T2, time)
        Step7(T1, time)
        Step8(T1, T4, time)
finally:
        GPIO.cleanup()