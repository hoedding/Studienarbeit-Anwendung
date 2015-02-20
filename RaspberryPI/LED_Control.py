#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting                          #
# Mail: mail[at]timohoeting.de  			   #
################################################

import sys
import time

from neopixel import *
from ConfigReader import *
import threading

#LED_COUNT   = 2      # Number of LED pixels. Get it from elsewhere, idiot.
LED_PIN     = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA     = 5       # DMA channel to use for generating signal (try 5)
LED_INVERT  = False   # True to invert the signal (when using NPN)


class NeoPixels(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		self.initStripe()

	def clear(self):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, Color(0,0,0))
			strip.show()

	def initStripe(self):
		# Neopixel Objekt erzeugen
		# LED_COUNT aus config holen
		reader = ConfigReader()
		LED_COUNT = int(reader.getNumberOfLED())
		global strip
		strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT)
		strip.begin()
		self.clear()

	def onePixel(self, number, red, green, blue):
		print ('Eine LED: #%d R:%d G:%d B:%d' % (number, red, green, blue))
		# Einen Pixel mit den o.g. RGB-Werten anschalten
		strip.setPixelColor(number, Color(red, green, blue))
		strip.show()

	def rangePixel(self, start, end, red, green, blue):
		print ('Mehrere LED: #%d - #%d R:%d G:%d B:%d'% (start, end, red, green, blue))
		for i in range(start, end):
			strip.setPixelColor(i, Color(red, green, blue))
			strip.show()

	def allPixel(self, red, green, blue):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, Color(red, green, blue))
			strip.show()

	def getCurrentColor(self, number):
		# Gibt den 24 Bit Farbwert zurück
		value = strip.getPixelColor(number)
		return value

	def getLedAsArray(self):
		colours = []
		colours = strip.getPixels()
		return colours

	def doBlinder(self):
		# Alle LEDs auf höchter Helligkeit anschalten (Farbe: Weis)
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, Color(255,255,255))
			strip.show()
		print 'blinder'

	def fadeAllIn(self, direction):
		# Eine LED nach der anderen Anschalten (Farbe: Weis)
		num = strip.numPixels()
		if direction == 0:
			for i in range(num):
				# von 0 bis num
				strip.setPixelColor(i, Color(255,255,255))
				strip.show()
				time.sleep( 0.5 )
		elif direction == 1:
			for i in range(num, 0):
				# von num bis 0
				strip.setPixelColor(i, Color(255,255,255))
				strip.show()
				time.sleep( 0.5 )

	def fadeAllOut(Self, direction):
		# Eine LED nach der anderen Ausschalten (Farbe: Weis)
		num = strip.numPixels()
		if direction == 0:
			for i in range(num):
				# von 0 bis num
				strip.setPixelColor(i, Color(0,0,0))
				strip.show()
				time.sleep( 0.5 )
		elif direction == 1:
			for i in range(num, 0):
				# von num bis 0
				strip.setPixelColor(i, Color(0,0,0))
				strip.show()
				time.sleep( 0.5 )

	def motionLight(self, direction):
		# Alle LEDs werden eingeschaltet und nach
		# bestimmten Zeitraum 'period' wieder ausgeschaltet
		reader = ConfigReader()
		period = reader.getTimePeriod()
		self.fadeAllIn(direction)
		time.sleep(period)
		self.fadeAllOut(direction)

	def colourRed(self):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, Color(255,0,0))
			strip.show()

	def colourGreen(self):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, Color(0,255,0))
			strip.show()

	def colourBlue(self):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, Color(0,0,255))
			strip.show()

	def dimmedWhite(self):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, Color(150,150,150))
			strip.show()

	def strobe(self):
		# TODO
		print 'strobe'

	def colourFader(self):
		# TODO
		print 'colourfader'

	def effectLED(self, code):
		# Einprogrammierte Effekte starten
		# 1 Alle an
		# 2 Alle aus
		# 3 Alle rot
		# 4 Alle grün
		# 5 Alle blau
		# 6 Alle gedimmt weis
		# 7 Strobo
		# 8 Bunte Übergänge
		if code == '1':
			self.fadeAllIn(0)
		elif code == '2':
			self.fadeAllOut(0)
		elif code == '3':
			self.colourRed()
		elif code == '4':
			self.colourGreen()
		elif code == '5':
			self.colourBlue()
		elif code == '6':
			self.dimmedWhite()
		elif code == '7':
			self.strobe()
		elif code == '8':
			self.colourFader()
