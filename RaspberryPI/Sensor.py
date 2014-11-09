#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting       				           #
# Mail: mail[at]timohoeting.de  				       #
################################################

import RPi.GPIO as GPIO
import time
# import der Pixelsteuerung
from runPixels import *
# import des ConfigReaders
from readConfig import *

class MotionDetection():
	def run(self):
		# Use BCM GPIO references
		# instead of physical pin numbers
		GPIO.setmode(GPIO.BCM)
		reader = ConfigReader()

		# Festlegen der beiden Detection-Pins
		MOTION_PIN1 = int(reader.getMotionPin1())
		MOTION_PIN2 = int(reader.getMotionPin1())

		# Diese als Input definieren
		GPIO.setup(MOTION_PIN1,GPIO.IN)
		GPIO.setup(MOTION_PIN2,GPIO.IN)

		# Status definieren um verschiedene Änderungen zu erkennen
		Current_State  = 0
		Previous_State = 0

		# Klasse zur Ansteuerung der LEDs initialisieren
		pixel = NeoPixels()
		pixel.initStripe()

		try:
			# Loop zur Erkennung einer Bewegung
			# Sensort erkennt Beweung -> Signal = High
			# Wartet 3 Sekunden und setzt Signal = Low
			while True :
				Current_State = GPIO.input(MOTION_PIN1)
				if Current_State == 1 and Previous_State == 0:
					print "Motion detected!"
					# Zum Test eine LED anschalten
					pixel.rangePixel(0, 2, 255, 255, 255)
					Previous_State=1
	    		elif Current_State == 0 and Previous_State == 1:
					print "Ready"
					# Und zum Test wieder ausschalten
					pixel.clear()
					Previous_State=0
				time.sleep(0.01)
		except KeyboardInterrupt:
		print "Quit"
		GPIO.cleanup()
