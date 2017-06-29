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
import pyvesc
from pyvesc import SetDutyCycle, SetRPM, GetRotorPosition, SetRotorPositionMode
from roverprocess.arm17.arm import Joints, Controller, Config, ManualControl,Sections,Limits
from math import pi
import serial

# Any libraries you need can be imported here. You almost always need time!
import time

base_max_speed = 4
base_min_speed = 0.2
shoulder_max_speed = 4
shoulder_min_speed = 0.2
elbow_max_speed = 4
elbow_min_speed = 0.2

device_keys = ["d_armBase", "d_armShoulder", "d_armElbow"]

dt = 0.1
BAUDRATE = 115200
SERIAL_TIMEOUT = 0.1

max_duty = 100000
# Constant for the duty curves
curve_val = 5

def duty_curve(f):
	''' scales a float to a suitable duty cycle value
		Args:
			f (float): value between -1 and 1.
		Returns:
			Float between -max_duty and max_duty
	'''
	a = ((curve_val**abs(f)) - 1)/(curve_val - 1)
	if f > 0:
		return a*max_duty
	else:
		return -a*max_duty

class ArmProcess(RoverProcess):

	def setup(self, args):
		for key in ["joystick1", "joystick2", "triggerR", "triggerL"]:
			self.subscribe(key)
		for key in device_keys:
			self.subscribe(key)
		self.base_direction = None
		self.joints_pos = Joints(0, pi/4, 0, 0, 0, 0)
		self.speeds = Joints(0,0,0,0,0,0)
		self.command = [0,0,0,0,0,0]
		section_lengths = Sections(
				upper_arm=0.35,
				forearm=0.42,
				end_effector=0.1)
		joint_limits = Joints(
				# in radians
				base=None,
				shoulder=None,
				elbow=None,
				wrist_pitch=None,
				wrist_roll=None,
				gripper=None)
		max_angular_velocity = Joints(
				base=0.2,
				shoulder=0.2,
				elbow=0.2,
				wrist_pitch=0.2,
				wrist_roll=0.2,
				gripper=0.2)
		self.config = Config(section_lengths, joint_limits, max_angular_velocity)
		self.controller = Controller(self.config)
		self.mode = ManualControl()
		self.devices = {}
		# joint_offsets are values in degrees to 'zero' the encoder angle
		self.joint_offsets = {"d_armShoulder":0, "d_armElbow":0}


	def simulate_positions(self):
		''' Updates the positions by calculating new values for testing.'''
		new_joints = list(self.joints_pos)
		for i in range(len(self.speeds)):
			if new_joints[i] is not None:
				new_joints[i] = self.joints_pos[i] + self.speeds[i] * dt
		return Joints(*new_joints)

	def poll_encoder(self, device):
		''' Polls each VESC for its encoder position.'''
		with serial.Serial(self.devices[device], baudrate=BAUDRATE, timeout=SERIAL_TIMEOUT) as ser:
			ser.write(pyvesc.encode_request(GetRotorPosition))
			while ser.in_waiting == 0:
				# Wait for response. TODO: Maybe don't wait forever...
				pass
			buffer = ser.readline()
			try:
				(response, consumed) = pyvesc.decode(buffer)
				if response.__class__ == GetRotorPosition:
					return response.rotor_pos
			except:
				self.log("Failed to read rotor position {}".format(device), "ERROR")
		return None

	def get_positions(self):
		''' Returns an updated Joints object with the current arm positions'''
		new_joints = list(self.joints_pos)
		for i, device in enumerate(["d_armShoulder", "d_armElbow"]):
			if device in self.devices:
				reading = self.poll_encoder(device)
				if reading is not None:
					reading += self.joint_offsets[device]
					new_joints[i+1] = pi*reading/360 #Convert to radians
				else:
					self.log("Could not read joint position {}".format(device), "WARNING")
		return Joints(*new_joints)

	def loop(self):
		self.joints_pos = self.get_positions()
		self.controller.user_command(self.mode, *Joints(*self.command))
		self.speeds = self.controller.update_duties(self.joints_pos)
		#publish speeds/duty cycles here
		self.log("joints_pos: {}".format(self.joints_pos))
		self.log("speeds: {}".format(self.speeds))
		self.send_duties()
		time.sleep(dt)

	def send_duties(self):
		''' Tell each motor controller to turn on motors'''
		if "d_armShoulder" in self.devices:
			with serial.Serial(self.devices["d_armShoulder"], baudrate=BAUDRATE, timeout=SERIAL_TIMEOUT) as ser:
				ser.write(pyvesc.encode(SetDutyCycle(int(100000*self.speeds[1]))))
		if "d_armElbow" in self.devices:
			with serial.Serial(self.devices["d_armElbow"], baudrate=BAUDRATE, timeout=SERIAL_TIMEOUT) as ser:
				ser.write(pyvesc.encode(SetDutyCycle(int(100000*self.speeds[2]))))


	def on_joystick1(self, data):
		''' Shoulder joint'''
		y_axis = data[1]
		y_axis = (y_axis * shoulder_max_speed)
		if y_axis > shoulder_min_speed or y_axis < -shoulder_min_speed:
			armShoulderSpeed = int(y_axis)
		else:
			armShoulderSpeed = 0
		self.command[1] = armShoulderSpeed

	def on_joystick2(self, data): #y-axis vertical motion of elbow, x-axis joint along the length of the elbow
		''' Elbow joints.'''
		y_axis = data[1]
		y_axis = (y_axis * elbow_max_speed)

		if y_axis > elbow_min_speed or y_axis < -elbow_min_speed:
			armY_ElbowSpeed = int(y_axis)
		else:
			armY_ElbowSpeed = 0
		self.command[2] = armY_ElbowSpeed

	def on_triggerR(self, trigger):
		''' Base rotation right'''
		trigger = -1*(trigger + 1)/2
		armBaseSpeed = trigger * base_max_speed/2
		if self.base_direction is "right" or self.base_direction is None:
			if -base_min_speed <armBaseSpeed < base_min_speed:
				armBaseSpeed = 0
				self.base_direction = None
			else:
				self.base_direction = "right"
			self.command[0] = armBaseSpeed


	def on_triggerL(self, trigger):
		''' Base rotation left'''
		trigger = (trigger + 1)/2
		armBaseSpeed = trigger * base_max_speed/2
		if self.base_direction is "left" or self.base_direction is None:
			if -base_min_speed <armBaseSpeed < base_min_speed:
				armBaseSpeed = 0
				self.base_direction = None
			else:
				self.base_direction = "left"
			self.command[0] = armBaseSpeed

	def messageTrigger(self, message):
		if message.key in device_keys:
			self.log("Received device: {}".format(message.key), "DEBUG")
			self.devices[message.key] = message.data
			with serial.Serial(message.data, baudrate=BAUDRATE, timeout=SERIAL_TIMEOUT) as ser:
				# Turn on encoder readings for this VESC
				ser.write(pyvesc.encode(
					SetRotorPositionMode(
						SetRotorPositionMode.DISP_POS_MODE_ENCODER )))







