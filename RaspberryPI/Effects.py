#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting       				           #
# Mail: mail[at]timohoeting.de  				       #
################################################

class effects():
	def runEffect(self, code, led):
		if code == '1':
			self.allon(led)
		elif code == '2':
			self.fadeallin(led)
		elif code == '3':
			self.fadeallout(led)
		elif code == '4':
			self.blinder(led)

	def allon(self, led):
		pixel.doBlinder()

	def fadeallin(self, led):
		pixel.fadeAllIn()

	def fadeallout(self, led):
		pixel.fadeAllOut()

	def blinder(self, led):
		pixel.doBlinder()
