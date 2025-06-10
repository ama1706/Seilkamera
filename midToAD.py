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
    a_to_mid()

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

def a_to_mid():
    steps_a = 1024
    steps_b = 1024
    steps_c = 1024
    steps_d = 1536

    time = 15
    time_a = time / steps_a / 8
    time_b = time / steps_b / 8
    time_c = time / steps_c / 8
    time_d = time / steps_d / 8

    th_motor_a = th.Thread(target=forwardA, args=(steps_a, A1, A2, A3, A4, time_a))
    th_motor_b = th.Thread(target=backwardB, args=(steps_b, B1,B2, B3, B4, time_b))
    th_motor_c = th.Thread(target=backwardC, args=(steps_c, C1, C2, C3, C4, time_c))
    th_motor_d = th.Thread(target=forwardD, args=(steps_d, D1, D2, D3, D4, time_d))

    th_motor_a.start()
    th_motor_b.start()
    th_motor_c.start()
    th_motor_d.start()

    th_motor_a.join()
    th_motor_b.join()
    th_motor_c.join()
    th_motor_d.join()

main()
