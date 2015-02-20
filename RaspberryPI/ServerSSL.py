#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting       		           #
# Mail: mail[at]timohoeting.de  		       #
################################################
import sys
import threading
import hashlib
from ConfigReader import *
from OpenSSL import SSL
from twisted.internet import reactor, ssl
from twisted.internet.protocol import Factory, Protocol

class LightServerSSL(Protocol):
    def connectionMade(self):
        # Es darf nur eine Netzwerkverbindung zum System bestehen
        # Falls eine weitere aufgebaut wird, so wird sie direkt wieder
        # gecancelt
        if (len(connections) >= 1):
            # TODO: Gibt den Fehler:
            # 2596:error:140790E5:SSL routines:SSL23_WRITE:ssl
            # handshake failure:/SourceCache/OpenSSL098/OpenSSL098-52/src/ssl/s23_lib.c:182:
            self.transport.loseConnection()
        else:
            connections.append(self)

    def connectionLost(self, reason):
        # Wenn die Verbindung getrennt wird, wird die Liste geleert
        # und die Verbindung im System beendet
        if self in connections:
            connections.remove(self)

    def dataReceived(self, line):
        file = datamanager.dataReceived(data)
        if (file != None):
            self.transport.write(file.read())

class StartLightServer(threading.Thread):
    def __init__(self, d):
        threading.Thread.__init__(self)
        global datamanager
        datamanager = d

    def run(self):
        global connections
        connections = []
        factory = Factory()
    	factory.protocol = LightServerSSL
    	reactor.listenSSL(7005, factory, ssl.DefaultOpenSSLContextFactory('./certs/server.key', './certs/server.crt'))
        # The default reactor, by default, will install signal handlers
        # to catch events like Ctrl-C, SIGTERM, and so on. However, you can't
        # install signal handlers from non-main threads in Python, which means
        # that reactor.run() will cause an error.
        # Pass the installSignalHandlers=0 keyword argument to reactor.run to
        # work around this.
    	reactor.run(installSignalHandlers=False)
