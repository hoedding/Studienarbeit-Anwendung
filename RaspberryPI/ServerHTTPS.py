#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting       				   #
# Mail: mail[at]timohoeting.de  			   #
################################################

from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
import cgi
from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
import hashlib
from ConfigReader import *
import threading
from twisted.internet import reactor, ssl

class LightServer(Resource):
  def render_POST(self, request):
    file = datamanager.dataReceived(cgi.escape(request.args["data"][0]))
    if (file != None):
        self.transport.write(file.read())

class StartLightServer(threading.Thread):
  def __init__(self, c):
     threading.Thread.__init__(self)
     global center
     center = c
     # TODO: Thread für Datamanager
     global datamanager
     datamanager = RecvdData()
     datamanager.init(center)

  def run(self):
     root = Resource()
     root.putChild("serv", LightServer())
     factory = Site(root)
     sslContext = ssl.DefaultOpenSSLContextFactory(
         './certs/server.key', './certs/server.crt'
     )
     reactor.listenSSL(8000, factory, contextFactory = sslContext)
     #reactor.listenTCP(8000, factory)
     reactor.run(installSignalHandlers=False)