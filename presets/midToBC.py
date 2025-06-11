try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:  # pragma: no cover - hardware dependency
    import fake_gpio as GPIO
from time import sleep
import threading as th
import json
from pathlib import Path


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

def main():
    gpio_lock = th.Lock()
    setup()
    
    steps_a = 1024
    steps_b = 1536
    steps_c = 1536
    steps_d = 1024

    time = 15
    time_a = time / steps_a / 8
    time_b = time / steps_b / 8
    time_c = time / steps_c / 8
    time_d = time / steps_d / 8

    th_motor_a = th.Thread(target=backwardA, args=(steps_a, A1, A2, A3, A4, time_a))
    th_motor_b = th.Thread(target=forwardB, args=(steps_b, B1,B2, B3, B4, time_b))
    th_motor_c = th.Thread(target=forwardC, args=(steps_c, C1, C2, C3, C4, time_c))
    th_motor_d = th.Thread(target=backwardD, args=(steps_d, D1, D2, D3, D4, time_d))

    th_motor_a.start()
    th_motor_b.start()
    th_motor_c.start()
    th_motor_d.start()

    th_motor_a.join()
    th_motor_b.join()
    th_motor_c.join()
    th_motor_d.join()

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

def backwardA(steps, A, B, C, D, time):
 
    count = 0
    min_time = 0.003
    smooth_start = steps * 0.1
    smooth_stop = steps * 0.9

    y = (min_time-time)/smooth_start
    time = min_time

    GPIO.setmode(GPIO.BCM)
    for i in range(steps):
        if count <= smooth_start:
            Step8(A, D, time)
            Step7(A, time)
            Step6(A, B, time)
            Step5(B, time)
            Step4(B, C, time)
            Step3(C, time)
            Step2(D, C, time)
            Step1(D, time)

            time = time - y
            count = count + 1
        elif count > smooth_start and count >= smooth_stop:
            Step8(A, D, time)
            Step7(A, time)
            Step6(A, B, time)
            Step5(B, time)
            Step4(B, C, time)
            Step3(C, time)
            Step2(D, C, time)
            Step1(D, time)

            time = time + y
            count = count + 1
        else:
            Step8(A, D, time)
            Step7(A, time)
            Step6(A, B, time)
            Step5(B, time)
            Step4(B, C, time)
            Step3(C, time)
            Step2(D, C, time)
            Step1(D, time)

            count = count + 1 


def forwardA(steps, A, B, C, D, time):
 
    count = 0
    min_time = 0.003
    smooth_start = steps * 0.1
    smooth_stop = steps * 0.9

    y = (min_time-time)/smooth_start
    time = min_time

    GPIO.setmode(GPIO.BCM)
    for i in range(steps):
        if count <= smooth_start:
            Step1(D, time)
            Step2(D, C, time)
            Step3(C, time)
            Step4(B, C, time)
            Step5(B, time)
            Step6(A, B, time)
            Step7(A, time)
            Step8(A, D, time)
            time = time - y
            count = count + 1
        elif count > smooth_start and count >= smooth_stop:
            Step1(D, time)
            Step2(D, C, time)
            Step3(C, time)
            Step4(B, C, time)
            Step5(B, time)
            Step6(A, B, time)
            Step7(A, time)
            Step8(A, D, time)
            time = time + y
            count = count + 1
        else:
            Step1(D, time)
            Step2(D, C, time)
            Step3(C, time)
            Step4(B, C, time)
            Step5(B, time)
            Step6(A, B, time)
            Step7(A, time)
            Step8(A, D, time)
            count = count + 1 


def backwardB(steps, A, B, C, D, time):
 
    count = 0
    min_time = 0.003
    smooth_start = steps * 0.1
    smooth_stop = steps * 0.9

    y = (min_time-time)/smooth_start
    time = min_time

    GPIO.setmode(GPIO.BCM)
    for i in range(steps):
        if count <= smooth_start:
            Step8(A, D, time)
            Step7(A, time)
            Step6(A, B, time)
            Step5(B, time)
            Step4(B, C, time)
            Step3(C, time)
            Step2(D, C, time)
            Step1(D, time)

            time = time - y
            count = count + 1
        elif count > smooth_start and count >= smooth_stop:
            Step8(A, D, time)
            Step7(A, time)
            Step6(A, B, time)
            Step5(B, time)
            Step4(B, C, time)
            Step3(C, time)
            Step2(D, C, time)
            Step1(D, time)

            time = time + y
            count = count + 1
        else:
            Step8(A, D, time)
            Step7(A, time)
            Step6(A, B, time)
            Step5(B, time)
            Step4(B, C, time)
            Step3(C, time)
            Step2(D, C, time)
            Step1(D, time)

            count = count + 1 


def forwardB(steps, A, B, C, D, time):
   
    count = 0
    min_time = 0.003
    smooth_start = steps * 0.1
    smooth_stop = steps * 0.9

    y = (min_time-time)/smooth_start
    time = min_time

    GPIO.setmode(GPIO.BCM)
    for i in range(steps):
        if count <= smooth_start:
            Step1(D, time)
            Step2(D, C, time)
            Step3(C, time)
            Step4(B, C, time)
            Step5(B, time)
            Step6(A, B, time)
            Step7(A, time)
            Step8(A, D, time)
            time = time - y
            count = count + 1
        elif count > smooth_start and count >= smooth_stop:
            Step1(D, time)
            Step2(D, C, time)
            Step3(C, time)
            Step4(B, C, time)
            Step5(B, time)
            Step6(A, B, time)
            Step7(A, time)
            Step8(A, D, time)
            time = time + y
            count = count + 1
        else:
            Step1(D, time)
            Step2(D, C, time)
            Step3(C, time)
            Step4(B, C, time)
            Step5(B, time)
            Step6(A, B, time)
            Step7(A, time)
            Step8(A, D, time)
            count = count + 1 



def backwardC(steps, A, B, C, D, time):
 
    count = 0
    min_time = 0.003
    smooth_start = steps * 0.1
    smooth_stop = steps * 0.9

    y = (min_time-time)/smooth_start
    time = min_time

    GPIO.setmode(GPIO.BCM)
    for i in range(steps):
        if count <= smooth_start:
            Step8(A, D, time)
            Step7(A, time)
            Step6(A, B, time)
            Step5(B, time)
            Step4(B, C, time)
            Step3(C, time)
            Step2(D, C, time)
            Step1(D, time)

            time = time - y
            count = count + 1
        elif count > smooth_start and count >= smooth_stop:
            Step8(A, D, time)
            Step7(A, time)
            Step6(A, B, time)
            Step5(B, time)
            Step4(B, C, time)
            Step3(C, time)
            Step2(D, C, time)
            Step1(D, time)

            time = time + y
            count = count + 1
        else:
            Step8(A, D, time)
            Step7(A, time)
            Step6(A, B, time)
            Step5(B, time)
            Step4(B, C, time)
            Step3(C, time)
            Step2(D, C, time)
            Step1(D, time)

            count = count + 1 


def forwardC(steps, A, B, C, D, time):
  
    count = 0
    min_time = 0.003
    smooth_start = steps * 0.1
    smooth_stop = steps * 0.9

    y = (min_time-time)/smooth_start
    time = min_time

    GPIO.setmode(GPIO.BCM)
    for i in range(steps):
        if count <= smooth_start:
            Step1(D, time)
            Step2(D, C, time)
            Step3(C, time)
            Step4(B, C, time)
            Step5(B, time)
            Step6(A, B, time)
            Step7(A, time)
            Step8(A, D, time)
            time = time - y
            count = count + 1
        elif count > smooth_start and count >= smooth_stop:
            Step1(D, time)
            Step2(D, C, time)
            Step3(C, time)
            Step4(B, C, time)
            Step5(B, time)
            Step6(A, B, time)
            Step7(A, time)
            Step8(A, D, time)
            time = time + y
            count = count + 1
        else:
            Step1(D, time)
            Step2(D, C, time)
            Step3(C, time)
            Step4(B, C, time)
            Step5(B, time)
            Step6(A, B, time)
            Step7(A, time)
            Step8(A, D, time)
            count = count + 1 

    


def backwardD(steps, A, B, C, D, time):

    count = 0
    min_time = 0.003
    smooth_start = steps * 0.1
    smooth_stop = steps * 0.9

    y = (min_time-time)/smooth_start
    time = min_time

    GPIO.setmode(GPIO.BCM)
    for i in range(steps):
        if count <= smooth_start:
            Step8(A, D, time)
            Step7(A, time)
            Step6(A, B, time)
            Step5(B, time)
            Step4(B, C, time)
            Step3(C, time)
            Step2(D, C, time)
            Step1(D, time)

            time = time - y
            count = count + 1
        elif count > smooth_start and count >= smooth_stop:
            Step8(A, D, time)
            Step7(A, time)
            Step6(A, B, time)
            Step5(B, time)
            Step4(B, C, time)
            Step3(C, time)
            Step2(D, C, time)
            Step1(D, time)

            time = time + y
            count = count + 1
        else:
            Step8(A, D, time)
            Step7(A, time)
            Step6(A, B, time)
            Step5(B, time)
            Step4(B, C, time)
            Step3(C, time)
            Step2(D, C, time)
            Step1(D, time)

            count = count + 1 


def forwardD(steps, A, B, C, D, time):

    count = 0
    min_time = 0.003
    smooth_start = steps * 0.1
    smooth_stop = steps * 0.9

    y = (min_time-time)/smooth_start
    time = min_time

    GPIO.setmode(GPIO.BCM)
    for i in range(steps):
        if count <= smooth_start:
            Step1(D, time)
            Step2(D, C, time)
            Step3(C, time)
            Step4(B, C, time)
            Step5(B, time)
            Step6(A, B, time)
            Step7(A, time)
            Step8(A, D, time)
            time = time - y
            count = count + 1
        elif count > smooth_start and count >= smooth_stop:
            Step1(D, time)
            Step2(D, C, time)
            Step3(C, time)
            Step4(B, C, time)
            Step5(B, time)
            Step6(A, B, time)
            Step7(A, time)
            Step8(A, D, time)
            time = time + y
            count = count + 1
        else:
            Step1(D, time)
            Step2(D, C, time)
            Step3(C, time)
            Step4(B, C, time)
            Step5(B, time)
            Step6(A, B, time)
            Step7(A, time)
            Step8(A, D, time)
            count = count + 1 


main()