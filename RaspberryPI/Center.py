#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting                          #
# Mail: mail[at]timohoeting.de                 #
################################################
# Center of Application

import sys
import logging
import time
import datetime
import threading
from ServerHTTPS import *
from Sensor import *
from LED_Control import *
from ApplePush import *
from ConfigWriter import *
from RecvdData import *
from ImageCreation import *

class Core():
  def init(self):
    # Alle Initialisierungen vornehmen
    # Server = Webserver, der die Eingaben der App empfängt
    # Sensor = Klasse, welche die Bewegungssensoren auswertet
    # LED = Klasse zur LED Steuerung
    # Server, Sensor, LED werden in eigenen Threads initialisiert
    # Modus = Aktueller Modus in dem sich das System befindet
    # System wird in Modus 0 initialisiert (Bewegungsmelder an)
    global datamanager
    datamanager =  RecvdData(self)
    datamanager.daemon = True
    threads.append(datamanager)
    global server
    server = StartLightServer(datamanager)
    server.daemon = True
    threads.append(server)
    global sensor
    sensor = MotionDetection(self)
    sensor.daemon = True
    threads.append(sensor)
    global led
    led = NeoPixels()
    led.daemon = True
    threads.append(led)
    global modus
    modus = 0
    self.startAll()
    self.startCamRecording()
    self.checkCertificates()

  def startAll(self):
    print '############# Studienarbeit Timo Höting #############'
    print '# Mail: mail[at]timohoeting.de                      #'
    print '# BW Cooperative State University Karlsruhe         #'
    print '#####################################################'
    try:
        datamanager.start()
    except:
        self.writeLog(str(arg))
    else:
        print '# Datenauswertung gestartet                         #'
    try:
        server.start()
    except:
        self.writeLog(str(arg))
    else:
        print '# Webserver gestartet.                              #'
    try:
        sensor.start()
    except:
        self.writeLog(str(arg))
    else:
        print '# Bewegungsüberwachung gestartet.                   #'
    try:
        led.start()
    except:
        self.writeLog(str(arg))
    else:
        print '# LEDs initialisiert.                               #'

  def startCamRecording(self):
    global imagecrea
    imagecrea = ImageCreation()
    imagecrea.daemon = True
    threads.append(imagecrea)
    try:
        imagecrea.start()
        imagecrea.setUser(_user)
    except IOError:
        self.writeLog(str(arg))
    try:
        imagecrea.createDirectory()
    except IOError:
        self.writeLog(str(arg))
    else:
        print '# Verzeichnis erzeugt oder vorhanden (FTP).         #'
    try:
        imagecrea.startRecording()
    except IOError:
        self.writeLog(str(arg))
    else:
        print '# Aufzeichnug der IP-Kamera gestartet.              #'
    try:
        imagecrea.removeOldFiles()
    except IOError:
        self.writeLog(str(arg))
    else:
        print '# Alte Bilder werden automatisch gelöscht.          #'

  def checkCertificates(self):
    global apnallowed
    apnallowed = True
    if os.path.exists("certs/Studienarbeit-APN.key.pem") == False:
        apnallowed = False
    if os.path.exists("certs/Studienarbeit-APN.crt.pem") == False:
        apnallowed = False
    if os.path.exists("certs/server.key") == False:
        apnallowed = False
    if os.path.exists("certs/server.crt") == False:
        apnallowed = False
    if apnallowed == True:
        print '# Alle APN-Zertifikate vorhanden.                   #'
    print '#####################################################'

  def getModus(self):
      return modus

  def setModus(self, mod):
      # Modus
      # 0: Beleuchtung wird durch Bewegungsmelder ausgelöst
      # 1: Beleuchtung wird manuell vom Benutzer über App gesteuert
      # 2: Bewegungsmelder als Alarmanlage, beim Auslösen wird der
      #    Benutzer benachrichtigt und Bild der Kamera als Notification
      #    auf dem Smartphone angezeigt
      global modus
      modus = mod
      print modus

  def motionDetected(self, direction):
    # Wird bei Auslösen des Bewegungssensors aufgerufen
    if(modus == 0):
        led.motionLight(direction)
    elif(modus == 2):
        self.alarm()

  def alarm(self):
      # Wird ausgelöst, wenn System im Modus 'Alarmanlage' ist
      # Meldung an Smartphone
      imagecrea.safeCurrentImages()
      self.writeLog('Bewegung ausgelöst!')
      ap = ApplePush()
      #ap.push("")

  def clearPixel(self):
    # Alle Pixel ausschalten
    led.clear()

  def getLEDStatusAsJson(self):
    led_values = led.getLedAsArray()
    print led_values
    print len(led_values)
    data = 'LED:{"led": ['
    count = 0
    if len(led_values) > 0:
        for i in range(0, len(led_values)-1):
            data = data + '{"l":"' + str(led_values[i]) + '"},'
            count = count + 1
        data = data + '{"l":"' + str(led_values[len(led_values)-1]) + '"}]}'
        count = count + 1
        print count
        return data

  def writeLog(self, content):
    # Message ins Logfile schreiben
    Ttime = time.time()
    formattedTime = datetime.datetime.fromtimestamp(Ttime).strftime('%Y-%m-%d %H:%M:%S')
    logging.basicConfig(filename='./log/all.log',level=logging.DEBUG)
    logging.warning(formattedTime + '| ' + content)

  def lightUpOneLED(self, ledNo, red, green, blue):
    # Eine einzelne LED mit den o.g. RGB-Werten dauerhaft anschalten
    if(modus == 1):
        led.onePixel(ledNo, red, green, blue)

  def lightUpLEDRange(self, rangeStart, rangeEnd, red, green, blue):
    # Einen Bereich von LEDs mit den o.g. RGB-Werten
    # dauerhaft einschalten
    if(modus == 1):
        led.rangePixel(rangeStart, rangeEnd, red, green, blue)

  def lightUpAllLED(self, red, green, blue):
    # Einen Bereich von LEDs mit den o.g. RGB-Werten
    # dauerhaft einschalten
    if(modus == 1):
        led.allPixel(red, green, blue)

  def effectLED(self, code):
    # Effekte auf einer LED aktivieren
    led.effectLED(code)

  def changeConfiguration(self, key, value):
      writer = ConfigWriter()
      if key == 'TOKEN':
          writer.addNewToken(value)
      elif key == 'pw':
          writer.changePassword(value)
      else:
          writer.changeConfig(key, value)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print 'Bitte Benutzer angeben:'
        print 'sudo python Center.py "user"'
        sys.exit(0)
    global _user
    _user = sys.argv[1]
    threads = []
    core = Core()
    core.init()
    try:
        while(1):
            time.sleep(0.01)
    except KeyboardInterrupt:
        print '#############  Anwendung wird beendet   #############'
        sensor.stop()
        print '# Bewegungsüberwachung beendet.                     #'
        # Threads beenden
        datamanager.join()
        print '# Datenauswertung beendet.                          #'
        server.join()
        print '# Webserver gestoppt.                               #'
        led.join()
        print '# Steuerung der LEDs beendet.                       #'
        imagecrea.join()
        print '# Aufnahme gestoppt.                                #'
        print '#####################################################'
