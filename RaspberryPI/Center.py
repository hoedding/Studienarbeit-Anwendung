#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting       				           #
# Mail: mail[at]timohoeting.de  				       #
################################################
# Center of Application

from Server import *
from Sensor import *



class Core():
  def init(self):
    # Alle Initialisierungen vornehmen
    # Server = Webserver, der die Eingaben der App empfängt
    # Sensor = Klasse, welche die Bewegungssensoren auswertet
    # Modus = Aktueller Modus in dem sich das System befindet
    global server
    server = StartLightServer()
    global sensor
    sensor = MotionDetection()
    self.start()
    global modus
    modus = 0

  def start(self):
    try:
      server.start(self)
    except IOError:
      print 'Error:', arg
    else:
      print 'Server gestartet'
    try:
      sensor.run(self)
    except IOError:
      print 'Error:', arg
    else:
      print 'Motion Detection gestartet'

  def motionDetected(self):
    # Zum Test eine LED anschalten
    pixel.rangePixel(0, 2, 255, 255, 255)
    print 'motion'

  def clearPixel(self):
    # Alle Pixel ausschalten
    print 'clear pixel'

  def getLedStatus(self):
    print 'led status'

if __name__ == "__main__":
    core = Core()
    core.init()
