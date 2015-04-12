#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting						  #
# Mail: mail[at]timohoeting.de				 #
################################################

import threading
import subprocess
import threading
from ConfigReader import *
import time
import os
import getpass

class ImageCreation(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def cleanup(self):
		# FTP unmounten
		ftppath = "/home/"+ currentuser + "/ftp"
		args = "umount " + ftppath
		subprocess.Popen([args], shell=True)

	def join(self):
		self.cleanup()
		threading.Thread.join(self)

	def setUser(self, _user):
		global currentuser
		currentuser = _user

	def createDirectory(self):
		directory = "/home/"+currentuser+"/ftp"
		dirAvaible = os.path.exists(directory)
		if dirAvaible == False:
			args = "mkdir " + directory
			subprocess.Popen([args], shell=True)
		self.mountFTP()
		dirAvaible = os.path.exists(directory + "/img")
		if dirAvaible == False:
			args = "mkdir " + directory + "/img"
			subprocess.Popen([args], shell=True)
		dirAvaible = os.path.exists(directory + "/safe")
		if dirAvaible == False:
			args = "mkdir " + directory + "/safe"
			subprocess.Popen([args], shell=True)

	def startRecording(self):
		path = '/home/'+currentuser+'/ftp'
		dirAvaible = os.path.exists(path)
		if dirAvaible:
			reader = ConfigReader()
			script = 'sh ./script/recordIpCam.sh '
			user = reader.getCamUser()
			pw = reader.getCamPassword()
			ip = reader.getCamHost()
			arguments = script + " " + path + " " + ip + " " + user + " " + pw
			subprocess.Popen([arguments], shell=True)

	def removeOldFiles(self):
		path = '/home/'+currentuser+'/ftp'
		dirAvaible = os.path.exists(path)
		if dirAvaible:
			script = 'sh ./script/remove.sh '
			arguments = script + " " + path
			subprocess.Popen([arguments], shell=True)

	def safeCurrentImages(self):
		path = '/home/'+currentuser+'/ftp'
		dirAvaible = os.path.exists(path)
		if dirAvaible:
			script = 'sh ./script/move.sh '
			arguments = script + " " + path
			subprocess.Popen([arguments], shell=True)

	def mountFTP(self):
		reader = ConfigReader()
		host = reader.getFTP()
		user = reader.getFTPUser()
		password = reader.getFTPPW()
		path = reader.getFTPDirectory()
		script = 'sh ./script/mountFTP.sh '
		arguments = script + " " + path + " " + host + " " + user + " " + password + " " + currentuser
		subprocess.Popen([arguments], shell=True)
