from re import X
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
import queue

# (x, y) are the center of the cup
# { = left, } = right
# + = up, - = down

def task3():
   # x= 0
    print("Thread 3 started. Waiting for the signal....")
    while True:
        try:
            robotMain.thread_switch_event.wait()
            print("Welcome to Auto Camera Mode.")
            robotMain.go_event.wait()
            print("Go*****************************************!!")
            if streamThread.x > 282:
                while streamThread.x > 282:
                    rcThread.deviceUC1.write('}')   #Right
                    time.sleep(1)
            elif streamThread.x < 282:
                while streamThread.x < 282:
                    rcThread.deviceUC1.write('{')   #Left
                    time.sleep(1)
            rcThread.deviceUC1.write('q')   #Stop (Break)
            print("Goal Achieved!")
            robotMain.go_event.clear()        #Stop auto mode. This thread will wait until go button is pressed again.
            for m in range(0, 10): 
              rcThread.client_sock.send('K')           #Send 'K' for clear to clear the go flag. We don't want the Android to keep sending 'go'
          
        except KeyboardInterrupt:
            print("\nDisconnected")
            raise SystemExit 