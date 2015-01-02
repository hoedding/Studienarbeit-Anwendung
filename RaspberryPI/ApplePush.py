#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting       				   #
# Mail: mail[at]timohoeting.de  			   #
################################################

import socket, ssl, json, struct
import binascii
from ConfigReader import *

class ApplePush():
    # Das Apple-Device bekommt eine Message und den Namen
    # des neu aufgenommen Fotos gepusht
    def push(self, message):
        reader = ConfigReader()
        deviceToken = reader.getToken()
        thePayLoad = {
                     'aps': {
                          'alert':'Hello world',
                          'sound':'default',
                          'badge':42,
                          },
                     'test_data': { 'foo': 'bar' },
                     }
        theCertfile = 'iphone_ck.pem'
        theHost = ( 'gateway.sandbox.push.apple.com', 2195 )
        data = json.dumps( thePayLoad )
        deviceToken = deviceToken.replace(' ','')
        byteToken = binascii.unhexlify(deviceToken)
        theFormat = '!BH32sH%ds' % len(data)
        theNotification = struct.pack( theFormat, 0, 32, byteToken, len(data), data )
        ssl_sock = ssl.wrap_socket( socket.socket( socket.AF_INET, socket.SOCK_STREAM ), certfile = theCertfile )
        ssl_sock.connect( theHost )
        ssl_sock.write( theNotification )
        ssl_sock.close()
