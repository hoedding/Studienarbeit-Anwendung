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
		# Einen Pixel mit den o.g. RGB-Werten anschalten
		strip.setPixelColor(number, Color(red, green, blue))
		strip.show()

	def rangePixel(self, start, end, red, green, blue):
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
		pixels = strip.getPixels()
		colours = []
		for i in range(0,strip.numPixels()):
			colours.append(pixels[i])
		return colours

	def doBlinder(self):
		# Alle LEDs auf höchter Helligkeit anschalten (Farbe: Weis)
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, Color(255,255,255))
		strip.show()

	def fadeAllIn(self, direction):
		# Eine LED nach der anderen Anschalten (Farbe: Weis)
		num = strip.numPixels()
		if direction == 0:
			for i in range(num):
				# von 0 bis num
				strip.setPixelColor(i, Color(255,255,255))
				strip.show()
				time.sleep( 0.025 )
		elif direction == 1:
			for i in range(num):
				# von num bis 0
				strip.setPixelColor(num-i, Color(255,255,255))
				strip.show()
				time.sleep( 0.025 )

	def fadeAllOut(Self, direction):
		# Eine LED nach der anderen Ausschalten (Farbe: Weis)
		num = strip.numPixels()
		if direction == 0:
			for i in range(num):
				# von 0 bis num
				strip.setPixelColor(i, Color(0,0,0))
				strip.show()
				time.sleep( 0.025 )
		elif direction == 1:
			for i in range(num):
				# von num bis 0
				strip.setPixelColor(num-i, Color(0,0,0))
				strip.show()
				time.sleep( 0.025 )

	def motionLight(self, direction):
		# Alle LEDs werden eingeschaltet und nach
		# bestimmten Zeitraum 'period' wieder ausgeschaltet
		reader = ConfigReader()
		period = reader.getTimePeriod()
		self.fadeAllIn(direction)
		time.sleep(float(period))
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

	def rainbow(self):
		# TODO
		print 'colourfader'

	def effectLED(self, code):
		# Einprogrammierte Effekte starten
		# 1 Strobo
		# 2 Bunte Farben
		if code == '1':
			self.strobe()
		elif code == '2':
			self.rainbow()
