import pygame
import time
import sys
sys.dont_write_bytecode = True # stops .pyc generation in subsequent imports
from Controller import Controller


def printAxes():    # print the status of all controller axes
	axes = controller.getAxes()
	roundedAxes = [round(i, 2) for i in axes]
	print("  Lx   Ly   Rx   Ry    T")
	print(roundedAxes)
	print("\n")

def printButtons():	# print the state of all controller buttons
	buttons = controller.getButtons()
	print(" A  B  X  Y  LB RB Bk St Ls Rs")
	print(buttons)
	print("\n")

def printDPad():	# print the state of the D Pad buttons
	dPad = controller.getDPad()
	print("L/R U/D")
	print(dPad)
	print("\n")

# program execution starts here
	
pygame.init()
controller = Controller(0)
if not controller.isConnected:
	print("Controller not detected.")
	time.sleep(1.5)
	exit()
	
while(True):
	pygame.event.pump()
	printAxes()
	printButtons()
	printDPad()
	time.sleep(0.25)
