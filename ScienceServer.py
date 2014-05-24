import math
import socket
import time
import subprocess
from ServoDriver import *

sciencePort = 3006

# do SCIENCE!
def runExperiment():
	experpos = 1700 # position to drop soil into experiment chamber
	samppos = 2100 # position to drop soil into sample chamber
	shakenum = 6 # number of times to "shake" servo before moving on
	shakeammount = 50
	command = "raspistill -q 75 -o /home/pi/pictures/" + time.strftime("%m%d%H%M%S", time.localtime()) + ".jpg"
	print("we are sciencing")
	#setup servo
	servoDriver = ServoDriver()
	#take picture
	subprocess.call(command, shell = True)
	#move to position to drop soil into experiment chamber
	servoDriver.setServo(4,experpos)
	
	time.sleep(0.5)
	
	
	# "shake" servo to get more soil in 
	for i in range(0,shakenum):
		servoDriver.setServo(4, experpos + shakeammount)
		time.sleep(0.1)
		servoDriver.setServo(4, experpos - 2*shakeammount)
		time.sleep(0.1)
		servoDriver.setServo(4, experpos + 2*shakeammount)
		time.sleep(0.2)
	time.sleep(1)
	
	#take picture every 2 seconds for a minute
	for n in range(0,29):
		subprocess.call(command, shell = True)
		time.sleep(2)

	print("Sciencing has been completed")
	# #move to position to drop soil into sample chamber
	# servoDriver.setServo(4,samppos)
	
	# # "shake" servo to get more soil in 
	# for i in range(0,shakenum)
		# servoDriver.setservo(4, samppos + shakeammount)
		# time.sleep(0.1)
		# servoDriver.setservo(4, samppos - 2*shakeammount)
		# time.sleep(0.1)
		# servoDriver.setservo(4, samppos + 2*shakeammount)
		# time.sleep(0.1)

	
def parseCommand(command):
	print(command)
	if command == "#RE":
		runExperiment()

def stopSockets(): # Stops sockets on error condition
	try:
		scienceSocket.close()
	except:
		pass
	try:
		serverSocket.close()
	except:
		pass


### Main Program ###

# set up logging
try:
	logfile = open("/home/pi/scienceLogs/" + time.strftime("%m%d%H%M%S", time.localtime()) + ".log", "w")
except:
	print("science logging failed!")

# set up GPIOs
# try:
	# GPIO.setwarnings(False)
	# GPIO.setmode(GPIO.BOARD)
	# GPIO.setup(11, GPIO.OUT) # stepper direction
	# GPIO.setup(13, GPIO.OUT) # stepper step
# except:
	# print("GPIO setup failed!")
	# raise
	# #subprocess.call("sudo reboot", shell = True)
	
# begin server connection
try:
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serverSocket.bind(("", sciencePort))
	serverSocket.listen(0)
	print("Science Server listening on port " + str(sciencePort))
	# main execution loop
	while(True):
		(scienceSocket, clientAddress) = serverSocket.accept()
		print("Science Server connected.")
		while(True):
			data = scienceSocket.recv(256)
			if(data == ""): # socket closing
				break
			else:
				parseCommand(data)
		print("Science Server disconnected.")
except KeyboardInterrupt:
	print("\nmanual shutdown...")
	stopSockets()
	#GPIO.cleanup()
except:
	stopSockets()
	#GPIO.cleanup()
	raise
