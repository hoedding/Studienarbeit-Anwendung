#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting       				   #
# Mail: mail[at]timohoeting.de  			   #
################################################


import sys
sys.path.insert(0, 'pycatapns')
from push import APNS_Push
from message import APNS_Message_Custom
from ConfigReader import *

class ApplePush():
    # Das Apple-Device bekommt eine Message und den Namen
    # des neu aufgenommen Fotos gepusht
    def push(self, message, data):
        push = APNS_Push(APNS_Push.ENVIRONMENT_SANDBOX, "Studienarbeit-APN.pem")
        push.setRootCertificationAuthority("Apple.pem")
        push.connect()

        message = APNS_Message_Custom('xxx')
        message.setCustomIdentifier("Message-Badge-3")
        message.setText('')
        message.setSound()
        message.setCustomProperty('acme2', ('bang', 'whiz'))
        message.setExpiry(30)
        message.setActionLocKey('Show me!')
        message.setLocKey('Bewegung erkannt! %1$@!')
        message.setLocArgs(('', 5))
        message.setLaunchImage('DefaultAlert.png')

        push.add(message)
        push.send()
        errors = push.getErrors()
        if len(errors) > 0:
        	print(errors)
        push.disconnect()
