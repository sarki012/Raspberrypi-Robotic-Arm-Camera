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

left_x = 0
left_y = 0
right_x = 0
right_y = 0
left_claw_x = 0
left_claw_y = 0
right_claw_x = 0
right_claw_y = 0

def task2():
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
                   # print(r)
                   # time.sleep(1)
                    if (r < 82):
                       # print(r)
                        #time.sleep(1)
                        left_x = x - r
                        left_y = y
                        right_x = x + r
                        right_y = y
                        string = str(x) + " " + str(y) 
                        left_string = str(left_x) + " " + str(left_y) 
                        right_string = str(right_x) + " " + str(right_y) 
                        # draw the circle in the output image, then draw a rectangle
                        # corresponding to the center of the circle
                        cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                        cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                        cv2.putText(output, string, (x, y), font, 0.75, (0, 0, 0))
                        cv2.putText(output, left_string, ((x - 150), y), font, 0.5, (0, 0, 0))
                        cv2.putText(output, right_string, ((x + r), (y + 50)), font, 0.5, (0, 0, 0))
                    # if x < 640 and y < 480:
                        color = frame[y, x]
                        #b,g,r = (frame[x,y])
                        blue = int(color[0])
                        green = int(color[1])
                        red = int(color[2])
                        string2 = "Red: {}, Green: {}, Blue: {}".format(red, green, blue)
                        cv2.putText(output, string2, (x - 100,(y+ 100)), font, 0.5, (0, 0, 0))
                    #(b, g, r) = frame[green_centerX, green_centerY]
          #  print("Pixel at (x, y) - Red: {}, Green: {}, Blue: {}".format(red, green, blue))  
                    
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

        #        M = cv2.moments(contour)
         #       if M['m00'] != 0.0:
          #          x = int(M['m10']/M['m00'])
           #         y = int(M['m01']/M['m00'])

           #     cv2.putText(frame, 'Circle', (x, y),
            #        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)


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
                        if(i == 0):
                            # text on topmost co-ordinate.
                          #  cv2.putText(frame, "Arrow tip", (x, y),
                           #                 font, 0.5, (255, 0, 0))
                            if x2 > 100 and x2 < 320 and y2 > 300 and y2 < 400:
                                cv2.putText(output, "Left Claw", ((x2 - 100), y2), 
                                    font, 0.5, (0, 0, 0))
                                left_claw_x = x2
                                left_claw_y = y2
                            elif x2 >= 320 and x2 < 640 and y2 > 300 and y2 < 400:
                                cv2.putText(output, "Right Claw", ((x2 - 100), y2), 
                                    font, 0.5, (0, 0, 0))
                                right_claw_x = x2
                                right_claw_y = y2
                            cv2.putText(output, string, (x2, y2), 
                                    font, 0.5, (0, 0, 0))
                       # else:
                            # text on remaining co-ordinates.
                        #    cv2.putText(frame, string, (x, y), 
                         #           font, 0.5, (0, 255, 0)) 
                    i = i + 1
            #print(ret)
            if ret != False and x != 0:
               # cv2.imshow("output", np.hstack([frame, output]))
                #cv2.waitKey(1)
                cv2.imshow('Image',output)
                cv2.waitKey(1)
              	# show the output image
            x = 1
        except KeyboardInterrupt:
            # When everything done, release the capture
            cap.release()
            cv2.destroyAllWindows()
            raise SystemExit    