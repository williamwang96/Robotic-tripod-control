import serial
import time
import pygame
import sys

import pygame

def manual_tracking():

	pygame.init()

	window = pygame.display.set_mode((800,600))

	pygame.display.set_caption("Window")

	black = (0,0,0)
	white=(255,255,255)

	x,y=0,0

	moveX,moveY=0,0

	clock = pygame.time.Clock()

	while True:

	    for event in pygame.event.get():

	        if (event.type==pygame.QUIT):
	        	exit()

	        if (event.type==pygame.KEYDOWN):
	            if (event.key==pygame.K_LEFT):
	                print('left')
	                moveX = -5
	            if (event.key==pygame.K_RIGHT):
	                print('right')
	                moveX = 5
	            if (event.key==pygame.K_UP):
	                moveY = -5
	            if (event.key==pygame.K_DOWN):
	                moveY = 5

	        if (event.type==pygame.KEYUP):
	            if (event.key==pygame.K_LEFT):
	                moveX=0
	            if (event.key==pygame.K_RIGHT):
	                moveX=0
	            if (event.key==pygame.K_UP):
	                moveY=0
	            if (event.key==pygame.K_DOWN):
	                moveY=0

	    window.fill(black)

	    x+=moveX
	    y+=moveY

	    pygame.draw.rect(window,white,(x,y,50,50))

	    clock.tick(50)

	    pygame.display.flip()

	pygame.quit()

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
	
	return ser

def close(ser):
	"""close the serial port passed in"""
	ser.close()
	print("Tripod control ends\n")


if __name__ == '__main__':
	manual_tracking()



#TODO
def auto_tracking(kite_dir, kite_angle, ser):
	"""Based on current kite position, turn the servo and keep the kite in the picture"""
	cur_pos = 0 #TODO current position of the camera
	#TODO send command to control the servo
	command = bytes([0xAA, kite_dir, kite_angle, cur_pos, 0x55])
	ser.write(command)
		
