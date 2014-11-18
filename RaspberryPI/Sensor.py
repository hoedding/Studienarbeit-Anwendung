#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting       				   #
# Mail: mail[at]timohoeting.de  			   #
################################################

import RPi.GPIO as GPIO
import time
# import des ConfigReaders
from ConfigReader import *
import threading

class MotionDetection(threading.Thread):
	def __init__(self, c):
		threading.Thread.__init__(self)
		global center
		center = c

	def run(self):
		# Use BCM GPIO references
		# instead of physical pin numbers
		GPIO.setmode(GPIO.BCM)
		reader = ConfigReader()

		# Festlegen der beiden Detection-Pins
		MOTION_PIN1 = int(reader.getMotionPin1())
		MOTION_PIN2 = int(reader.getMotionPin2())

		# Diese als Input definieren
		GPIO.setup(MOTION_PIN1,GPIO.IN)
		GPIO.setup(MOTION_PIN2,GPIO.IN)

		# Status definieren um verschiedene Änderungen zu erkennen
		Current_State  = 0
		Previous_State = 0

		try:
			center.writeLog('Motion Detection Status: OK')
			# Loop zur Erkennung einer Bewegung
			# Sensort erkennt Bewegung -> Signal = High
			# Wartet 3 Sekunden und setzt Signal = Low
			# TODO weitere Sensoren implementieren
			while True :
				Current_State = GPIO.input(MOTION_PIN1)
				if Current_State == 1 and Previous_State == 0:
					center.motionDetected()
					Previous_State = 1
				elif Current_State == 0 and Previous_State == 1:
					# Die LEDs werden nach bestimmter Zeit wieder
					# ausgeschaltet. Dies passiert in der Center-Klasse
					Previous_State=0
				time.sleep(0.01)
		except KeyboardInterrupt:
			print "Quit"
			GPIO.cleanup()
