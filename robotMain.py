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
import streamThread
import feedbackThread

if __name__ == "__main__":

    # creating threads
    t1 = threading.Thread(target=rcThread.task1, name='t1')
    t2 = threading.Thread(target=rcThread.task2, name='t2') 
    t3 = threading.Thread(target=streamThread.task3, name='t3') 
 
    # starting threads
    t1.start()
    time.sleep(1)
    t2.start()
    t3.start()
 
    # wait until all threads finish
    t1.join()
    t2.join()
    t3.join()