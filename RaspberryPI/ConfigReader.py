#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting       				           #
# Mail: mail[at]timohoeting.de  				       #
################################################

import ConfigParser

class ConfigReader():
	def getNumberOfLED(self):
		config = ConfigParser.ConfigParser()
		config.read("./config.ini")
		return config.get("common", "number")

	def getHashPass(self):
		config = ConfigParser.ConfigParser()
		config.read("./config.ini")
		return config.get("common", "passhash")

	def getMotionPin1(self):
		config = ConfigParser.ConfigParser()
		config.read("./config.ini")
		return config.get("common", "motion1")

	def getMotionPin2(self):
		config = ConfigParser.ConfigParser()
		config.read("./config.ini")
		return config.get("common", "motion2")

	def camAvaible(self):
		config = ConfigParser.ConfigParser()
		config.read("./config.ini")
		return config.get("cam", "avaible")

  	def camURL(self):
		config = ConfigParser.ConfigParser()
		config.read("./config.ini")
		return config.get("cam","url")

	def camShortURL(self):
		config = ConfigParser.ConfigParser()
		config.read("./config.ini")
		return config.get("cam","shorturl")

	def getTimePeriod(self):
		config = ConfigParser.ConfigParser()
		config.read("./config.ini")
		return int(config.get("led","motionOn"))
