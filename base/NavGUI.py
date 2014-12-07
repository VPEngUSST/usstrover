#Import all of the thread modules
from threads.communicationThread import communicationThread
from threads.inputThread import inputThread
from threads.navigationThread import navigationThread
from threads.panelThread import panelThread

#Import modules needed for GUI communication
import baseMessages
import json
from Queue import Queue
import time
import threads.unicodeConvert

#imports for Kivy GUI
import kivy
from kivy.app import App
from kivy.lang import Builder
#Turn off fullscreen - alternatively use 'fake' for borderless
from kivy.config import Config
Config.set('graphics', 'fullscreen', '0')
from kivy.core.window import Window
Window.size = (1000,600)
#Scheduler (for GUI related threading)
from kivy.clock import Clock

#import refrenced GUI components
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label


import time

convert = threads.unicodeConvert.convert

class NavigationApp(App):
	def build(self):
		#Set up clock to run function as 'threads'
		Clock.schedule_interval(self.displayQueue, 0.1)
		#self.update = Clock.schedule_interval(self.updateUI, 0.2)
		#build gui layout
		self.root = Builder.load_file('gui/nav.kv')
		self.layout = self.AppLayout()
		return self.root
	
	#In code references of Kv widgets
	class AppLayout(FloatLayout):
		pass
		
		# Button handler based off button.func property
	def buttonHandler(self, func):
		
		#Default action
		if(func == 'none'):
			print('Info: Button has no function')
		
	#test to display an amt of Queue items on label
	def displayQueue(self, amt):
		if not self.mailbox.empty():
			#self.ltb2.l_text
			data = str(self.mailbox.get())
			print(data)
		else:
			pass
			#print("no data in queue")
			
	def on_start(self):
		#Set up Queue
		self.mailbox = Queue()
			
		#Set up the threads
		self.commThread = communicationThread()
		self.inputThread = inputThread()
		self.navThread = navigationThread()
		self.panelThread = panelThread()
		
		#Any thread configuration options are run here
		self.commThread.sendPort = 8001
		self.commThread.receivePort = 8000
		self.commThread.sendInterval = 0.25
		self.commThread.inputThread = self.inputThread
		self.commThread.navThread = self.navThread
		self.commThread.panelThread = self.panelThread
		self.commThread.guiThread = self
		self.inputThread.commThread = self.commThread
		
		#Load the other threads
		print("starting")
		self.startThreads()
	
	def startThreads(self):
		self.commThread.start()
		self.inputThread.start()
		self.navThread.start()
		self.panelThread.start()

	def stopThreads(self):
		self.inputThread.stop()
		time.sleep(0.2)
		self.commThread.stop()
		self.navThread.stop()
		self.panelThread.stop()
		
	def on_stop(self):
		print('exiting')
		#Unload all threads
		self.stopThreads()


#Main App
NavigationApp().run()