#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting       				           #
# Mail: mail[at]timohoeting.de  				       #
################################################

from runPixels import *
from neopixel import *

class effects():
	def runEffect(self, code, pixel):
		if code == '1':
			self.allon(pixel)
		elif code == '2':
			self.fadeallin(pixel)
		elif code == '3':
			self.fadeallout(pixel)
		elif code == '4':
			self.blinder(pixel)

	def allon(pixel):
		pixel.doBlinder()

	def fadeallin(self, pixel):
		pixel.fadeAllIn()

	def fadeallout(self, pixel):
		pixel.fadeAllOut()

	def blinder(self, pixel):
		pixel.doBlinder()
