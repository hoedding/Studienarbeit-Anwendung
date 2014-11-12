#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting       				           #
# Mail: mail[at]timohoeting.de  				       #
################################################

from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
import hashlib
from ConfigReader import *

class LightServer(Protocol):
	def connectionMade(self):
		self.factory.clients.append(self)

	def connectionLost(self, reason):
		self.factory.clients.remove(self)

	def dataReceived(self, data):
		# Protokoll: auth:control:ledNo:rangeStart:rangeEnd:red:green:blue:effect:effectcode:hashv
		# Beispiel: admin:X00:1:0:0:10:10:10:0:0:58acb7acccce58ffa8b953b12b5a7702bd42dae441c1ad85057fa70b
		# Ermoeglicht Zuweisung von Farben und Effekte
		# Abruf des aktuellen Status sollte ebenfalls moeglich sein
		# zum Beispiel nach Neustart der App
		#
		# Ankommende String bei ":" aufsplitten und in Array a[] Speichern:
		a = data.split(':')
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
			effect = 	a[8]
			effectcode = a[9]
			hashv = a[10]
			data = auth + control + ledNo + rangeStart + rangeEnd + red + green + blue + effect + effectcode
			data = data.rstrip('\n')
			data = data.rstrip('\r')
			if (self.checkAuthentification(auth) & self.checkTransmissionData(data, hashv)):
				if control == 'X00':
					## Alle LEDs ausschalten
					central.clearPixel()
				elif control == 'X01':
					## Eine LED anschalten
					self.lightUpOneLED(int(ledNo), int(red), int(green), int(blue))
				elif control == 'X02':
					## LED Bereich anschalten
					self.lightUpLEDRange(int(rangeStart), int(rangeEnd), int(red), int(green), int(blue))
				elif control == 'X03':
					## Effekte eine LED
					print 'effekt X03'
				elif control == 'X04':
					## Effekte LED Bereich
					print 'effekt X04'
				elif control == 'X05':
					## Fest programmierte Effekte
					## z.B.: alle LEDs an
					central.runEffects(effectcode)
			else:
				print central.writeLog('Übertragung fehlerhaft')

	def lightUpOneLED(self, ledNo, red, green, blue):
		# Eine einzelne LED mit den o.g. RGB-Werten dauerhaft anschalten
		a = self.checkColorRange(red)
		b = self.checkColorRange(green)
		c = self.checkColorRange(blue)
		d = self.checkRange(ledNo)
		if ( a & b & c & d):
			central.lightUpOneLED(ledNo, red, green, blue)

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
			central.rangePixel(rangeStart, rangeEnd, red, green, blue)

	def effectOneLED(self):
    # Effekte auf einer LED aktivieren
		central.effectOneLED()

	def effectLEDRange(self):
		# Effekte auf einem LED-Bereich aktivieren
		central.effectLEDRange()

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
		return True

class StartLightServer():
  def start(central):
    factory = Factory()
    factory.clients = []
    factory.protocol = LightServer
    reactor.listenTCP(7002, factory)
    reactor.run()
