import serial
import time
import pygame
import sys
import pygame
from time import sleep

########################## Variables for Adjusting #################################
port = 'COM3'
baudrate = 19200  # default is 19200
timeout = 1.5  # default is 1.5

import cv2
import numpy as np
def get_key(img_key = np.array((0,0))):
    cv2.namedWindow('Robo Tripod Control', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Robo Tripod Control', 300, 150)
    cv2.imshow('Robo Tripod Control',img_key)
    k=cv2.waitKey(1)
    return k

def manual_tracking(servo):
    print('\nReady to control tripod\n')
    print('Press W S A D for up down left right')
    print('Press X to exit\n')
    moveX,moveY = 0,0
    # servo angles and moving
    angle1,angle2 = 90,90 # 1 is horizontal angle, 2 is vertical angle

    while True:        
        limit = True
        change = False

        key = get_key()

        if key == ord('a'):
            print('left')
            moveX = -5
        if key == ord('d'):
            print('right')
            moveX = 5
        if key == ord('w'):
            print('up')
            moveY = -5
        if key == ord('s'):
            print('down')
            moveY = 5
        if key == ord('x'):
            break
        if key == -1:
            moveX = 0
            moveY = 0

        # update servo postion
        angle1 -= moveX
        angle2 -= moveY

        if angle1 < 0:
            angle1 = 0
        elif angle1 > 180:
            angle1 = 180
        elif(angle2 < 0):
            angle2 = 0
        elif(angle2 > 180):
            angle2 = 180
        else:
            limit = False
            change = True

        if moveX != 0 or moveY != 0:
            if change:
                cmd = bytes([126,126,angle2,angle1])    
                servo.write(cmd)
                #print('cmd sent')
            moveX = 0
            moveY = 0
            print(f'Horizontal angle {angle1}')
            print(f'Vertical angle {angle2}')
            if limit:
                print('HIT LIMIT')
            print('')

        '''
        slp_time = 0.04 - (time.time()-t0)
        if slp_time > 0:
            sleep(slp_time)
        '''


def setup(port, baudrate=19200, timeout=1.5):
    """Set up the COM port, open it, and return it"""
    ser = serial.Serial()
    ser.port = port
    ser.baudrate = baudrate
    ser.timeout = timeout

    if not ser.isOpen():
        ser.open()

    print("Waiting for COM port to open...")
    sleep(3)

    if ser:
        print("\nCOM port opens successfully")

    print("Initializing servo...")
    cmd=bytes([126,126,90,90]) 
    for i in range(0,5):
        ser.write(cmd)
    sleep(1)

    return ser

def close(ser):
    """close the serial port passed in"""
    ser.close()
    print("Tripod control ends\n")

def main():
    servo = setup(port=port, baudrate=baudrate, timeout=timeout)
    manual_tracking(servo)
    close(servo)

#TODO
def auto_tracking(kite_dir, kite_angle, ser):
    """Based on current kite position, turn the servo and keep the kite in the picture"""
    cur_pos = 0 #TODO current position of the camera
    #TODO send command to control the servo
    command = bytes([0xAA, kite_dir, kite_angle, cur_pos, 0x55])
    ser.write(command)

if __name__ == '__main__':
    #manual_tracking()
    '''
    while True:
        key=get_key()
        if key!=-1:
            print(key)
        if key==ord('s'):
            break
    '''
    main()