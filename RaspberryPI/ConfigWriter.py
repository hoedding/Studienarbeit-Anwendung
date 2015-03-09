#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting       				   #
# Mail: mail[at]timohoeting.de  	           #
################################################

import json

class ConfigWriter():
    def changeConfig(self, key, value):
        jsonFile = open("config.json", "r")
        jdata = json.load(jsonFile)
        jsonFile.close()
        jdata[key] = value
        jsonFile = open("config.json", "w+")
        jsonFile.write(json.dumps(jdata))
        jsonFile.close()

    def addNewToken(self, token):
        jsonFile = open("tokenlist.json", "r")
        jdata = json.load(jsonFile)
        jsonFile.close()
        jdata['token'].append({"t":token})
        jsonFile = open("tokenlist.json", "w+")
        jsonFile.write(json.dumps(jdata))
        jsonFile.close()
