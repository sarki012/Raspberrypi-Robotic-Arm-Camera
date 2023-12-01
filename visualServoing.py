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


#x = 0       #Center of cup
#y = 0

#claw_center_x = 0       #Center of midpoint between tips of claw
#claw_center_y = 0

# { = left, } = right
# + = up, - = down

def task3():
    x= 0
    print("Thread 3 started. Waiting for the signal....")
    while True:
        try:
            x = robotMain.queue.get()
            robotMain.queue.task_done()
            robotMain.thread_switch_event.wait()
          #  print("Welcome to Auto Camera Mode.")
            robotMain.go_event.wait()
           # print("Go*****************************************!!")
            #while abs(282 - x) > 5:
            print("x", x)
            print("xC", 282)
          #  while abs(282 - x) > 25:
            #   if x > 0 and x < 640 and 282 > 0 and 282 < 640:
            if x > 282:
                while x > 282:
                    x = robotMain.queue.get()
                    robotMain.queue.task_done()
                    #print("x = ", x)
                    #time.sleep(1)
                    rcThread.deviceUC1.write('}')   #Right
                  #  print("Moving Right!")
            elif x < 282:
                while x < 282:
                    x = robotMain.queue.get()
                    robotMain.queue.task_done()
                    # print("x = ", x)
                    # time.sleep(1)
                    rcThread.deviceUC1.write('{')   #Left
                   # print("Moving Left!")
            rcThread.deviceUC1.write('q')   #Stop (Break)
            print("Goal Achieved!")
            robotMain.go_event.clear()
          
        except KeyboardInterrupt:
            print("\nDisconnected")
            raise SystemExit 