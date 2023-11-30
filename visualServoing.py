from pylibftdi import Device
import os
import glob
import time
from bluetooth import *
import socket
import bluetooth
import cv2
import numpy as np
import tty, sys, termios
import threading
import streamThread
import robotMain
import rcThread
from threading import Event
import signal

#x = 0       #Center of cup
#y = 0

#claw_center_x = 0       #Center of midpoint between tips of claw
#claw_center_y = 0

# { = left, } = right
# + = up, - = down

def task3():
    print("Thread 3 started. Waiting for the signal....")
    while True:
        try:
            robotMain.thread_switch_event.wait()
            print("Welcome to Auto Camera Mode.")
            robotMain.go_event.wait()
            print("Go*****************************************!!")
            error = streamThread.claw_center_x - streamThread.x
            while abs(error) > 5:
                if streamThread.x > 0 and streamThread.x < 640 and streamThread.claw_center_x > 0 and streamThread.claw_center_x < 640:
                    if streamThread.claw_center_x < (streamThread.x - 5):
                        rcThread.deviceUC1.write('}')   #Right
                    elif streamThread.claw_center_x > (streamThread.x + 5):
                        rcThread.deviceUC1.write('{')   #Left
                    if(abs(error) <= 5):
                        rcThread.deviceUC1.write('q')   #Stop (Break)
                        while True:
                            pass
        except KeyboardInterrupt:
            print("\nDisconnected")
            raise SystemExit 