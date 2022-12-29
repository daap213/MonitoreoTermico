#!/usr/bin/env python3
import serial
from time import sleep
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)
    ser.reset_input_buffer()

    while True:
        received_data = ser.read()              #read serial port
        sleep(0.03)
        data_left = ser.inWaiting()             #check for remaining byte
        received_data += ser.read(data_left)
        print (received_data)                   #print received data
        ser.write("aver")                #transmit data serially 
