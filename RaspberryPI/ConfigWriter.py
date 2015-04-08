#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting       				   #
# Mail: mail[at]timohoeting.de  	           #
################################################

import json
import hashlib

class ConfigWriter():
    def changeConfig(self, key, value):
        jsonFile = open("config.json", "r")
        jdata = json.load(jsonFile)
        jsonFile.close()
        jdata[key] = value
        jsonFile = open("config.json", "w+")
        jsonFile.write(json.dumps(jdata))
        jsonFile.close()

    def changePassword(self, value):
        hashpw = hashlib.sha224(value).hexdigest()
        jsonFile = open("config.json", "r")
        jdata = json.load(jsonFile)
        jsonFile.close()
        jdata["pw"] = hashpw
        jsonFile = open("config.json", "w+")
        jsonFile.write(json.dumps(jdata))
        jsonFile.close()
        print 'passwort geändert: ' + value

    def addNewToken(self, token):
        jsonFile = open("tokenlist.json", "r")
        jdata = json.load(jsonFile)
        jsonFile.close()
        tokens = jdata['token']
        for element in tokens:
            if element['t'] == token:
                return
        jdata['token'].append({"t":token})
        jsonFile = open("tokenlist.json", "w+")
        jsonFile.write(json.dumps(jdata))
        jsonFile.close()
