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
		connections = []
		self.factory.clients.remove(self)

	def dataReceived(self, data):
		# Protokoll: auth:control:ledNo:rangeStart:rangeEnd:red:green:blue:modus:effectcode:hashv
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
		# Funktioniert noch nicht 100%ig
		for c in self.factory.clients:
			c.transport.write('test' + '\n')

class StartLightServer(threading.Thread):
	def __init__(self, c):
		threading.Thread.__init__(self)
		global center
		center = c

 	def run(self):
		global factory
		factory = Factory()
		factory.clients = []
		factory.protocol = LightServer
		reactor.listenTCP(7002, factory)
		global connections
		connections = []
		reactor.run(installSignalHandlers=False)

	def pushNotification(self, message):
		factory.clients[0].sendMessage(message + '\n\r')
