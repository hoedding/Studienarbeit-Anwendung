#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting       				   #
# Mail: mail[at]timohoeting.de  			   #
################################################

import ConfigParser
import json

class ConfigReader():
	def getNumberOfLED(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata["number"]

	def getHashPass(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata["passhash"]

	def getMotionPin1(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata["motion1"]

	def getMotionPin2(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata["motion2"]

	def camAvaible(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata["avaible"]

  	def camURL(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata["url"]

	def camShortURL(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata["shorturl"]

	def getFTP(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata["ftp"]

	def getTimePeriod(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata["motionTime"]

	def getToken(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata["token"]
