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
		return jdata["ledcount"]

	def getHashPass(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata["passhash"]

	def getMotionPin1(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata["motionport1"]

	def getMotionPin2(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata["motionport2"]

	def camAvaible(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata["camavaible"]

  	def camURL(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata["cam_url"]

	def camShortURL(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata["cam_url_short"]

	def getFTP(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata["ftp_url"]

	def getTimePeriod(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata["timeperiod"]

	def getToken(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata["token"]
