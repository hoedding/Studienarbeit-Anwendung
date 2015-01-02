#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting       				   #
# Mail: mail[at]timohoeting.de  	           #
################################################

import json

class ConfigWriter():
    def change(self, key, value):
        if key == 'number':
            self.setNumberOfLED(value)
        elif key == 'username':
            self.setUser(value)
        elif key == 'passhash':
            self.setHash(value)
        elif key == 'motion1':
            self.setMotionPin1(value)
        elif key == 'motion2':
            self.setMotionPin2(value)
        elif key == 'avaible':
            self.setCamAvaible(value)
        elif key == 'url':
            self.setCamURL(value)
        elif key == 'short':
            self.setCamShortURL(value)
        elif key == 'ftp':
            self.setFTP(value)
        elif key == 'motionTime':
            self.setTimePeriod(value)

    def setNumberOfLED(self, m):
        jsonFile = open("config.json", "r")
        jdata = json.load(jsonFile)
        jsonFile.close()
        jdata["number"] = m
        jsonFile = open("config.json", "w+")
        jsonFile.write(json.dumps(jdata))
        jsonFile.close()

    def setUser(self, m):
        jsonFile = open("config.json", "r")
        jdata = json.load(jsonFile)
        jsonFile.close()
        jdata["username"] = m
        jsonFile = open("config.json", "w+")
        jsonFile.write(json.dumps(jdata))
        jsonFile.close()

    def setHash(self, m):
        jsonFile = open("config.json", "r")
        jdata = json.load(jsonFile)
        jsonFile.close()
        jdata["passhash"] = m
        jsonFile = open("config.json", "w+")
        jsonFile.write(json.dumps(jdata))
        jsonFile.close()

    def setMotionPin1(self, m):
        jsonFile = open("config.json", "r")
        jdata = json.load(jsonFile)
        jsonFile.close()
        jdata["motion1"] = m
        jsonFile = open("config.json", "w+")
        jsonFile.write(json.dumps(jdata))
        jsonFile.close()

    def setMotionPin2(self, m):
        jsonFile = open("config.json", "r")
        jdata = json.load(jsonFile)
        jsonFile.close()
        jdata["motion2"] = m
        jsonFile = open("config.json", "w+")
        jsonFile.write(json.dumps(jdata))
        jsonFile.close()

    def setCamAvaible(self, m):
        jsonFile = open("config.json", "r")
        jdata = json.load(jsonFile)
        jsonFile.close()
        jdata["avaible"] = m
        jsonFile = open("config.json", "w+")
        jsonFile.write(json.dumps(jdata))
        jsonFile.close()

    def setCamURL(self, m):
        jsonFile = open("config.json", "r")
        jdata = json.load(jsonFile)
        jsonFile.close()
        jdata["url"] = m
        jsonFile = open("config.json", "w+")
        jsonFile.write(json.dumps(jdata))
        jsonFile.close()

    def setCamShortURL(self, m):
        jsonFile = open("config.json", "r")
        jdata = json.load(jsonFile)
        jsonFile.close()
        jdata["short"] = m
        jsonFile = open("config.json", "w+")
        jsonFile.write(json.dumps(jdata))
        jsonFile.close()

    def setFTP(self, m):
        jsonFile = open("config.json", "r")
        jdata = json.load(jsonFile)
        jsonFile.close()
        jdata["ftp"] = m
        jsonFile = open("config.json", "w+")
        jsonFile.write(json.dumps(jdata))
        jsonFile.close()

    def setTimePeriod(self, m):
        jsonFile = open("config.json", "r")
        jdata = json.load(jsonFile)
        jsonFile.close()
        jdata["motionTime"] = m
        jsonFile = open("config.json", "w+")
        jsonFile.write(json.dumps(jdata))
        jsonFile.close()
