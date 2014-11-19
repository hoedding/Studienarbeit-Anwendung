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
from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver

class TLSServer(LineReceiver):
    def lineReceived(self, line):
        print "received: " + line

        if line == "STARTTLS":
            print "-- Switching to TLS"
            self.sendLine('READY')
            ctx = ServerTLSContext(
                privateKeyFileName='./certs/server.key',
                certificateFileName='./certs/server.crt',
                )
            self.transport.startTLS(ctx, self.factory)
            connections.append(self)
        else:
            a = line.split(':')
            print a
            if len(a) > 1:
                auth = 		a[0]
                control = 	a[1]
                ledNo = 	a[2]
                rangeStart = a[3]
                rangeEnd = 	a[4]
                red = 		a[5]
                green = 	a[6]
                blue = 		a[7]
                modus = 	a[8]
                effectcode = a[9]
                hashv = a[10]
                data = auth + control + ledNo + rangeStart + rangeEnd + red + green + blue + modus + effectcode
                data = data.rstrip('\n')
                data = data.rstrip('\r')
                if (self.checkAuthentification(auth) & self.checkTransmissionData(data, hashv)):
                    if control == 'X00':
                        ## Alle LEDs ausschalten
                        center.clearPixel()
                    elif control == 'X01':
                        ## Eine LED anschalten
                        self.lightUpOneLED(int(ledNo), int(red), int(green), int(blue))
                    elif control == 'X02':
                        ## LED Bereich anschalten
                        self.lightUpLEDRange(int(rangeStart), int(rangeEnd), int(red), int(green), int(blue))
                    elif control == 'X03':
                        ## Effekt alle LEDs
                        self.effectLED(effectcode)
                    elif control == 'X04':
                        ## Modus des Systems
                        self.changeModus(int(modus))
                else:
                    print center.writeLog('Übertragung fehlerhaft')

    def changeModus(self, modus):
        center.setModus(modus)


    def lightUpOneLED(self, ledNo, red, green, blue):
        # Eine einzelne LED mit den o.g. RGB-Werten dauerhaft anschalten
        a = self.checkColorRange(red)
        b = self.checkColorRange(green)
        c = self.checkColorRange(blue)
        d = self.checkRange(ledNo)
        if ( a & b & c & d):
            center.lightUpOneLED(ledNo, red, green, blue)

    def lightUpLEDRange(self, rangeStart, rangeEnd, red, green, blue):
        # Einen Bereich von LEDs mit den o.g. RGB-Werten
        # dauerhaft einschalten
        # Bereich muss ueberprueft werden mit checkRange()
        a = self.checkColorRange(red)
        b = self.checkColorRange(green)
        c = self.checkColorRange(blue)
        d = self.checkRange(rangeStart)
        e = self.checkRange(rangeEnd)
        if ( a & b & c & d & e):
            center.rangePixel(rangeStart, rangeEnd, red, green, blue)

    def effectLED(self, code):
            # Effekte auf einer LED aktivieren
            center.effectLED(code)

    def checkRange(self, ledNo):
        # Ueberprueft ob die uebergeben LED-Nummer ueberhaupt im
        # gueltigen Bereich liegt
        # Es wird der Eintrag 'number' aus dem Config-File geladen
        reader = ConfigReader()
        number = int(reader.getNumberOfLED())
        if ( ledNo >= 0 & ledNo < number):
            return True
        else:
            return False

    def checkColorRange(self, color):
        # Überprüfung ob Farbwert im gültigen Bereich liegt
        if (color >= 0 & color <= 255):
            return True
        return False

    def checkAuthentification(self, auth):
        # Authentifizierung überprüfen
        # Eingabewert ist das Passwort aus der Übertragung
        # Dieses wird gehasht und mit dem in der Konfiguration gespeicherten
        # Hashwert verglichen
        reader = ConfigReader()
        hashv = reader.getHashPass()
        pw = hashlib.sha224(auth).hexdigest()
        if ( pw == hashv ):
            return True
        return False

    def checkTransmissionData(self, data, check):
        # Korrektheit der Übertragung mittels Hashvergleich feststellen
        # Eingabewert sind die gesamten Daten der Übertragung
        hashdata = hashlib.sha224(data).hexdigest()
        check = check.rstrip('\n')
        check = check.rstrip('\r')
        if ( hashdata == check ):
            return True
        # Für Testübertragung return immer True
        return True

    def sendMessage(self, message):
        self.sendLine(message)

class ServerTLSContext(ssl.DefaultOpenSSLContextFactory):
    def __init__(self, *args, **kw):
        kw['sslmethod'] = SSL.TLSv1_METHOD
        ssl.DefaultOpenSSLContextFactory.__init__(self, *args, **kw)

class StartLightServer(threading.Thread):
    def __init__(self, c):
        threading.Thread.__init__(self)
        global center
        center = c

    def run(self):
        global factory
        factory = ServerFactory()
        factory.protocol = TLSServer
        reactor.listenTCP(7005, factory)
        global connections
        connections = []
        reactor.run(installSignalHandlers=False)

    def pushNotification(self, message):
        # Funktioniert nicht
        for c in connections:
            c.sendLine('con con con')
