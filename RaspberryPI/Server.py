#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting                          #
# Mail: mail[at]timohoeting.de                 #
################################################

from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
import hashlib
import threading

class LightServer(Protocol):
    def connectionMade(self):
        # Es darf nur eine Netzwerkverbindung zum System bestehen
        # Falls eine weitere aufgebaut wird, so wird sie direkt wieder
        # gecancelt
        if (len(connections) >= 1):
            self.transport.loseConnection()
        else:
            connections.append(self)
            self.factory.clients.append(self)

    def connectionLost(self, reason):
        # Wenn die Verbindung getrennt wird, wird die Liste geleert
        # und die Verbindung im System beendet
        if self in connections:
            connections.remove(self)
            self.factory.clients.remove(self)

    def dataReceived(self, data):
        file = datamanager.dataReceived(data)
        if (file != None):
            self.transport.write(file.read())

class StartLightServer(threading.Thread):
    def __init__(self, d):
        threading.Thread.__init__(self)
        global datamanager
        datamanager = d

    def run(self):
        global factory
        factory = Factory()
        factory.clients = []
        factory.protocol = LightServer
        reactor.listenTCP(7002, factory)
        global connections
        connections = []
        reactor.run(installSignalHandlers=False)
