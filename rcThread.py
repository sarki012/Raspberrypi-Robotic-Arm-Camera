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

def task1():
    cmd = 'sudo hciconfig hci0 piscan'
    os.system(cmd)

    wait = 0.001
    #F4:42:8F:10:5F:5F
    connection = False
    server_sock=BluetoothSocket( RFCOMM )
    server_sock.bind(("",PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    #uuid = "00001101-0000-1000-8000-00805F9B34FB"
    advertise_service( server_sock, "raspberrypi",
                    service_id = uuid,
                    service_classes = [ uuid, SERIAL_PORT_CLASS ],
                    profiles = [ SERIAL_PORT_PROFILE ]  
                        )

    filedescriptors = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin)
    deviceUC1 = Device('FT7210GA')     #Bottom USB
    deviceUC1.baudrate = 115200
    deviceUC1.open()
    deviceUC2 = Device('FT71VG2G')     #Top USB
    deviceUC2.baudrate = 115200
    deviceUC2.open()
    while True:
        if(connection == False):
            print("Waiting for connection on RFCOMM channel %d" % port)
            client_sock, client_info = server_sock.accept()
            connection = True
            print("Accepted connection from ", client_info)
        try:  
            data = client_sock.recv(50)
            if len(data) == 0:
                break
            data_char = chr(data[0])
            if data_char == 'u':        #Up
                deviceUC1.write('u')
            elif data_char == 'd':      #Down
                deviceUC1.write('d')
            elif data_char == '@':      #Stop boom
                deviceUC1.write('@')
            elif data_char == 'l':      #Left
                deviceUC1.write('l')
            elif data_char == 'r':      #Right
                deviceUC1.write('r')
            elif data_char == '$':      #Stop rotation
                deviceUC1.write('$')
            elif data_char == 'o':      #Out
                deviceUC2.write('o')
            elif data_char == 'i':      #In
                deviceUC2.write('i')
            elif data_char == '*':      #Stop Stick
                deviceUC2.write('*')
            elif data_char == 't':      #Tip down
                deviceUC2.write('t')
            elif data_char == 'p':      #Tip up
                deviceUC2.write('p')
            elif data_char == '^':      #Stop tip motor
                deviceUC2.write('^')
            elif data_char == 'n':      #CLaw open
                deviceUC2.write('n')
            elif data_char == 'c':      #Claw closed
                deviceUC2.write('c')
            elif data_char == '%':      #Stop claw motor
                deviceUC2.write('%')
        except KeyboardInterrupt:
            print("\nDisconnected")
            client_sock.close()
            server_sock.close()
            raise SystemExit 