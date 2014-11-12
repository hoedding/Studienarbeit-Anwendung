#!/usr/bin/env python
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

### Protocol Implementation

# This is just about the simplest possible protocol
class Echo(Protocol):
  def dataReceived(self, data):
    self.transport.write(data)

class StartTestServer():
  def start(self):
    control = center
    f = Factory()
    f.protocol = Echo
    reactor.listenTCP(8000, f)
    reactor.run()
