#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting                          #
# Mail: mail[at]timohoeting.de                 #
################################################

import ConfigParser
import json

class ConfigReader():
    def getValue(self, key):
        if key == "token":
            return self.getToken()
        data = open('config.json')
        jdata = json.load(data)
        return jdata[key]

    def getToken(self):
        data = open('tokenlist.json')
        jdata = json.load(data)
        return jdata["token"]
