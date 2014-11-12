#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting       				           #
# Mail: mail[at]timohoeting.de  				       #
################################################

import sys
import time

from neopixel import *
from ConfigReader import *

#LED_COUNT   = 2      # Number of LED pixels. Get it from elsewhere, idiot.
LED_PIN     = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA     = 5       # DMA channel to use for generating signal (try 5)
LED_INVERT  = False   # True to invert the signal (when using NPN)


class NeoPixels():
	def clear(self):
		print 'clear'
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

	def getCurrentColor(self, number):
		# Gibt den 24 Bit Farbwert zurück
		value = strip.getPixelColor(number)
		return value

  def getAllColours(self):
    number = strip.numPixels()
    colours[]
    for i in range(strip.numPixels()):
      colours.append(strip.getPixelColor(i))
    return colours

	def doBlinder(self):
		# Alle LEDs auf höchter Helligkeit anschalten (Farbe: Weis)
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, Color(255,255,255))
			strip.show()
		print 'blinder'

	def fadeAllIn(self):
		# Eine LED nach der anderen Anschalten (Farbe: Weis)
		# TODO: Richtung festlegen
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, Color(255,255,255))
			strip.show()
			time.sleep( 0.5 )
		print 'fadeAllIn'


	def fadeAllOut(Self):
		# Eine LED nach der anderen Ausschalten (Farbe: Weis)
		# TODO: Richtung festlegen
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, Color(0,0,0))
			strip.show()
			time.sleep( 0.5 )
		print 'fadeALlOut'
