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
            font = cv2.FONT_HERSHEY_COMPLEX
            ret, frame = cap.read()
            #src = cv2.resize(src, (1000, 750)) 
            # Convert image to gray and blur it
            src_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            src_gray = cv2.blur(src_gray, (3,3))
            canny_output = cv2.Canny(src_gray, 50, 150)
            contours, _ = cv2.findContours(
            canny_output, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  
            m = 0
            #using drawContours() function
            # list for storing names of shapes
            for contour in contours:
                approx = cv2.approxPolyDP(contour, 0.009 * cv2.arcLength(contour, True), True)
                # here we are ignoring first counter because 
                # findcontour function detects whole image as shape
                if m == 0:
                    m = 1
                    continue            
                # using drawContours() function
                cv2.drawContours(frame, [contour], -1, (0, 0, 255), 5)
                # Used to flatten the array containing
                # the co-ordinates of the vertices.
                n = approx.ravel() 
                i = 0
            
                for j in n :
                    if(i % 2 == 0):
                        x = n[i]
                        y = n[i + 1]
            
                        # String containing the co-ordinates.
                        string = str(x) + " " + str(y) 
            
                        if(i == 0):
                            # text on topmost co-ordinate.
                          #  cv2.putText(frame, "Arrow tip", (x, y),
                           #                 font, 0.5, (255, 0, 0)) 
                            cv2.putText(frame, string, (x, y), 
                                    font, 0.75, (0, 0, 0))
                        else:
                            # text on remaining co-ordinates.
                            cv2.putText(frame, string, (x, y), 
                                    font, 0.5, (0, 255, 0)) 
                    i = i + 1
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