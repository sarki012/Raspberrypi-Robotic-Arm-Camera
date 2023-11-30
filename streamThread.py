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
import rcThread

x = 0       #Center of cup
y = 0

claw_center_x = 0       #Center of midpoint between tips of claw
claw_center_y = 0


def task4():
    global left_x
    global left_y
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
            frame = cv2.resize(frame, (640, 480))
            output = frame.copy()
            width, height, channels = frame.shape
            #src = cv2.resize(src, (1000, 750)) 
            # Convert image to gray and blur it
            src_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            src_gray = cv2.blur(src_gray, (3,3))
           # canny_output = cv2.Canny(src_gray, 50, 150)
            canny_output = cv2.Canny(src_gray, 50, 150)
            contours, _ = cv2.findContours(
            canny_output, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  
            m = 0
            # detect circles in the image
            circles = cv2.HoughCircles(src_gray, cv2.HOUGH_GRADIENT, 1.2, 100)
            # ensure at least some circles were found
            if circles is not None:
                # convert the (x, y) coordinates and radius of the circles to integers
                circles = np.round(circles[0, :]).astype("int")
                # loop over the (x, y) coordinates and radius of the circles
                for (x, y, r) in circles:
                    string = "D(x,y)= " + "(" + str(x) + ", " + str(y) + ")" 
                    # draw the circle in the output image, then draw a rectangle
                    # corresponding to the center of the circle
                    cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                    cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                    cv2.putText(output, string, (x - 100, y - 20), font, 1, (0, 0, 0), thickness = 3)

            left_claw_x = 100
            left_claw_y = 250
            right_claw_x = 465
            right_claw_y = 300
            cv2.rectangle(output, (75, 225),(125,275),(255,0,0),5)
            cv2.rectangle(output, (left_claw_x - 5, left_claw_y - 5), (left_claw_x + 5, left_claw_y + 5), (0, 128, 255), -1)
            string = "A(x,y)= " + "(" + str(left_claw_x) + ", " + str(left_claw_y) + ")" 
            cv2.putText(output, string, (left_claw_x - 75, left_claw_y - 40), font, 1, (0, 0, 0), thickness = 3)
            cv2.rectangle(output, (440, 275),(490,325),(255,0,0),5) 
            cv2.rectangle(output, (right_claw_x - 5, right_claw_y - 5), (right_claw_x + 5, right_claw_y + 5), (0, 128, 255), -1)
            string = "B(x,y)= "
            cv2.putText(output, string, (right_claw_x + 20, right_claw_y), font, 1, (0, 0, 0), thickness = 3)
            string = "(" + str(right_claw_x) + ", " + str(right_claw_y) + ")"
            cv2.putText(output, string, (right_claw_x + 20, right_claw_y + 40), font, 1, (0, 0, 0), thickness = 3)
            cv2.line(output, (left_claw_x, left_claw_y), (right_claw_x, right_claw_y), (0, 255, 0), 5)
            claw_center_x = 282
            claw_center_y = 275
            string = "C(x,y)= "
            cv2.rectangle(output, (claw_center_x - 5, claw_center_y - 5), (claw_center_x + 5, claw_center_y + 5), (0, 128, 255), 5)
            cv2.putText(output, string, (claw_center_x - 50, claw_center_y + 40), font, 1, (0, 0, 0), thickness = 3)
            string = "(" + str(claw_center_x) + ", " + str(claw_center_y) + ")" 
            cv2.putText(output, string, (claw_center_x - 50, claw_center_y + 80), font, 1, (0, 0, 0), thickness = 3)
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
                cv2.drawContours(output, [contour], -1, (0, 0, 255), 5)

              #  M = cv2.moments(contour)
               # if M['m00'] != 0:
                #    cx = int(M['m10']/M['m00'])
                 #   cy = int(M['m01']/M['m00'])
                  #  cv2.circle(output, (cx, cy), 7, (0, 0, 255), -1)
                   # cv2.putText(output, "center", (cx - 20, cy - 20),
                    #        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                #print(f"x: {cx} y: {cy}")

                                # Used to flatten the array containing
                # the co-ordinates of the vertices.
                n = approx.ravel() 
                i = 0
            
                for j in n :
                    if(i % 2 == 0):
                        x2 = n[i]
                        y2 = n[i + 1]
                        # String containing the co-ordinates.
                        string = str(x2) + " " + str(y2) 
                    #    if(i == 0):
                            # text on topmost co-ordinate.
                          #  cv2.putText(frame, "Arrow tip", (x, y),
                           #                 font, 0.5, (255, 0, 0))
                          #  if x2 > 100 and x2 < 320 and y2 > 300 and y2 < 400:
              #              cv2.putText(output, "Left Claw", ((x2 - 100), y2), 
               #                     font, 0.5, (0, 0, 0))
                #            left_claw_x = x2
                 #           left_claw_y = y2
                        #elif x2 >= 320 and x2 < 640 and y2 > 300 and y2 < 400:
                  #          cv2.putText(output, "Right Claw", ((x2 - 100), y2), 
                   #                 font, 0.5, (0, 0, 0))
                    #        right_claw_x = x2
                     #       right_claw_y = y2
                      #      cv2.putText(output, string, (x2, y2), 
                       #             font, 0.5, (0, 0, 0))
                       # else:
                            # text on remaining co-ordinates.
                        #    cv2.putText(frame, string, (x, y), 
                         #           font, 0.5, (0, 255, 0)) 
                    i = i + 1

            
            if ret != False and x != 0:
                cv2.imshow('Image',output)
                cv2.waitKey(1)
              	# show the output image
            x = 1
        except KeyboardInterrupt:
            # When everything done, release the capture
            cap.release()
            cv2.destroyAllWindows()
            raise SystemExit    