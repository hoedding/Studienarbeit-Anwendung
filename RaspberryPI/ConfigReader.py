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

	def getLEDPort(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata["ledport"]

	def getHashPass(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata["pw"]

	def getUserName(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata["username"]

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

	def getFTP(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata["ftp_host"]

	def getTimePeriod(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata["timeperiod"]

	def getToken(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata["token"]

	def getTokenList(self):
		data = open('tokenlist.json')
		jdata = json.load(data)
		return jdata['token']

	def getFTPDirectory(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata['ftp_directory']

	def getFTPUser(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata['ftp_user']

	def getFTPPW(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata['ftp_pw']

	def getCamUser(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata['cam_user']

	def getCamPassword(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata['cam_pw']

	def getCamHost(self):
		data = open('config.json')
		jdata = json.load(data)
		return jdata["cam_host"]
