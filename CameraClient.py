
# A library to communicate with the rover's camera systems
# Added by Jordan

	# dependency list

import socket
import time
import sys


	# class definition

class CameraClient: # class to handle camera feeds	
	def __init__(self, IP, port):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.IP = IP
		self.port = port
		self.commandCameraStart = "#CS"
		self.commandCameraEnd = "#CE"

	def connect(self, retries):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.settimeout(1.0)
		try:
			self.socket.connect((self.IP, self.port))
			connected = True
			print("Connected CameraClient to " + self.IP + ":" + str(self.port))
			return True
		except socket.error:
			pass
		for i in range (0, retries):
			time.sleep(1)
			try:
				self.socket.connect((self.IP, self.port))
				connected = True
				print("Connected CameraClient to " + self.IP + ":" + str(self.port))
				return True
			except socket.error:
				pass
		sys.stderr.write("Could not connect CameraClient to " + self.IP + ":" + str(self.port))
		return False
	
	def startCamera(self):
		try:
			self.socket.send(self.commandCameraStart)
			return True
		except socket.error as e:
			print(e)
			return False
	
	def stopCamera(self):
		try:
			self.socket.send(self.commandCameraEnd)
			return True
		except socket.error as e:
			print(e)
			return False

	def test(self):
		try:
			self.socket.settimeout(0.05)
			self.socket.send("TST")
			return True
		except socket.error:
			return False

