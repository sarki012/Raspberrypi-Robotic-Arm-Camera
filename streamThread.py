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

def task2():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 5)

    if cap.isOpened():
        print("Video Capture Opened")

    x = 0
    while True:
        try:
            ret, frame = cap.read()
            #src = cv2.resize(src, (1000, 750)) 
            # Convert image to gray and blur it
            src_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            src_gray = cv2.blur(src_gray, (3,3))
            canny_output = cv2.Canny(src_gray, 50, 150)
            contours, _ = cv2.findContours(
            canny_output, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  
            i = 0
            #using drawContours() function
            # list for storing names of shapes
            for contour in contours:
                # here we are ignoring first counter because 
                # findcontour function detects whole image as shape
                if i == 0:
                    i = 1
                    continue            
                # using drawContours() function
                cv2.drawContours(frame, [contour], -1, (0, 0, 255), 20)
            
            #print(ret)
            if ret != False and x != 0:
                cv2.imshow('Image',frame)
                cv2.waitKey(1)
            x = 1
        except KeyboardInterrupt:
            # When everything done, release the capture
            cap.release()
            cv2.destroyAllWindows()
            raise SystemExit    