#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting       				   #
# Mail: mail[at]timohoeting.de  			   #
################################################

import sys, time
from apns import APNs, Frame, Payload
from ConfigReader import *

class ApplePush():
    def __init__(self):
        reader = ConfigReader()
        tokenlist = reader.getTokenList()
        global token
        token = []
        # Alle Tokens werden aus der Liste geladen
        for i in tokenlist:
            token.append(i['t'])

    # Das Apple-Device bekommt eine Message gepusht
    def push(self, message):
        if apnallowed == False:
            return
        # Developer Zertifikat für iOS Push Benachrichtigung
        apns = APNs(use_sandbox=True, cert_file='certs/Studienarbeit-APN.crt.pem', key_file='certs/Studienarbeit-APN.key.pem')
        payload = Payload(alert="Bewegung erkannt!", sound="default", badge=1)
        for i in token:
            apns.gateway_server.send_notification(i, payload)
