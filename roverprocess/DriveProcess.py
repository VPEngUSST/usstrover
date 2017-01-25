# Copyright 2016 University of Saskatchewan Space Design Team Licensed under the
# Educational Community License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may
# obtain a copy of the License at
#
# https://opensource.org/licenses/ecl2.php
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS"
# BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing
# permissions and limitations under the License.

from .RoverProcess import RoverProcess
import roverprocess.vesc as vesc
from roverprocess.vesc.messages.pwm import Pwm


class DriveProcess(RoverProcess):

    # Subscribed to joystick1 and joystick2.
	def getSubscribed(self):
		return ["joystick1", "joystick2"]

	def setup(self, args):
		for key in ["joystick1", "joystick2"]:
			self.subscribe(key)

	# Function that grabs the x and y axis values in message, then formats the data
	#  and prints the result to stdout.
	# Returns the newly formated x and y axis values in a new list
	def on_joystick1(self, message):
		y_axis = message[1]
		y_axis = (y_axis * 40000/2) # half power for testing
		if y_axis > 11000 or y_axis < -11000:
			newMessage = int(y_axis)
		else:
			newMessage = 0

		# print(newMessage)
		self.publish("wheel1", vesc.messages.base.VESCMessage.encode(Pwm(newMessage)))
		self.publish("wheel2", vesc.messages.base.VESCMessage.encode(Pwm(newMessage)))
		self.publish("wheel3", vesc.messages.base.VESCMessage.encode(Pwm(newMessage)))



	# Function that grabs the x and y axis values in message, then formats the data
	#  and prints the result to stdout.
	# Returns the newly formated x and y axis values in a new list
	def on_joystick2(self, message):
		y_axis = message[1]
		y_axis = (y_axis * 40000/2)
		if y_axis > 11000 or y_axis < -11000:
			newMessage = int(y_axis)
		else:
			newMessage = 0
		# print(newMessage)
		self.publish("wheel4", vesc.messages.base.VESCMessage.encode(Pwm(newMessage)))
		self.publish("wheel5", vesc.messages.base.VESCMessage.encode(Pwm(newMessage)))
		self.publish("wheel6", vesc.messages.base.VESCMessage.encode(Pwm(newMessage)))











