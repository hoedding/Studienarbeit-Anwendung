#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting                          #
# Mail: mail[at]timohoeting.de                 #
################################################

import hashlib
from ConfigReader import *
import threading

class RecvdData(threading.Thread):
    def __init__(self, c):
        threading.Thread.__init__(self)
        global center
        center = c

    def dataReceived(self, data):
        # Protokoll: user:pw:control:ledNo:rangeStart:rangeEnd:red:green:blue:modus:effectcode:config:hashv
        # Beispiel: admin:w:X00:1:0:0:10:10:10:0:0:w-w:58acb7acccce58ffa8b953b12b5a7702bd42dae441c1ad85057fa70b
        # Ermoeglicht Zuweisung von Farben und Effekten
        # Ermöglicht Abruf von aktuellem Status des Systems und der LEDs
        #
        # Ankommende String bei ":" aufsplitten und in Array a[] Speichern:
        a = data.split(':')
        print a
        if len(a) > 1:
            user =         a[0]
            pw =         a[1]
            control =     a[2]
            ledNo =     a[3]
            rangeStart = a[4]
            rangeEnd =     a[5]
            red =         a[6]
            green =     a[7]
            blue =         a[8]
            modus =     a[9]
            effectcode = a[10]
            config = a[11]
            hashv = a[12]
            data = user + pw + control + ledNo + rangeStart + rangeEnd + red + green + blue + modus + effectcode + config
            data = data.rstrip('\n')
            data = data.rstrip('\r')
            if (self.checkAuthentification(user, pw) & self.checkTransmissionData(data, hashv)):
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
                    ## Eine Farbe für alle LED
                    self.lightUpAllLED(int(red), int(green), int(blue))
                elif control == 'X04':
                    ## Effekt alle LEDs
                    self.effectLED(effectcode)
                elif control == 'X05':
                    ## Modus des Systems
                    self.changeModus(int(modus))
                elif control == 'X06':
                    ## Systemstatus als JSON an den Client
                    return self.sendStatus()
                elif control == 'X07':
                    ## Status der einzelnen LEDs senden
                    return self.sendLEDStatus()
                elif control == 'X08':
                    ## Konfiguration ändern
                    self.changeConfiguration(config)
                elif control == 'X09':
                    ## Login
                    return "LOGIN:TRUE"
            else:
                print center.writeLog('Übertragung fehlerhaft')

    def changeModus(self, modus):
        if modus >= 0 & modus < 4:
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

    def lightUpAllLED(self, red, green, blue):
        # Alle LEDs mit den o.g. RGB-Werten
        # dauerhaft einschalten
        # Bereich muss ueberprueft werden mit checkRange()
        a = self.checkColorRange(red)
        b = self.checkColorRange(green)
        c = self.checkColorRange(blue)
        if ( a & b & c):
            center.lightUpAllLED(red, green, blue)

    def effectLED(self, code):
        # Effekte auf einer LED aktivieren
        center.effectLED(code)

    def checkRange(self, ledNo):
        # Ueberprueft ob die uebergeben LED-Nummer ueberhaupt im
        # gueltigen Bereich liegt
        # Es wird der Eintrag 'number' aus dem Config-File geladen
        reader = ConfigReader()
        number = int(reader.getValue("ledcount"))
        if ( ledNo >= 0 & ledNo < number):
            return True
        else:
            return False

    def checkColorRange(self, color):
        # Überprüfung ob Farbwert im gültigen Bereich liegt
        if (color >= 0 & color <= 255):
            return True
        return False

    def checkAuthentification(self, user, pw):
        # Authentifizierung überprüfen
        # Eingabewert ist das Passwort aus der Übertragung
        # Dieses wird gehasht und mit dem in der Konfiguration gespeicherten
        # Hashwert verglichen
        reader = ConfigReader()
        hashv = reader.getValue("pw")
        pwd = hashlib.sha224(pw).hexdigest()
        user = reader.getValue("username")
        if ( pwd == hashv ):
            if ( user == user ):
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
        # TODO Für Testübertragung return immer True
        return True

    def sendStatus(self):
        # Status des Systems senden
        reader = ConfigReader()
        message = 'STATUS:{"ledcount":"' + reader.getValue("ledcount") + '","motionport1":"' + reader.getValue("motionport1") + '","motionport2":"' + reader.getValue("motionport2") + '","camavaible":"'
        message = message + reader.getValue("camavaible") + '","timeperiod":"' + reader.getValue("timeperiod") + '","ftpdir":"' + reader.getValue("ftp_directory") + '","ftphost":"' + reader.getValue("ftp_host")
        message = message + '","camuser":"' + reader.getValue("cam_user") + '","ftpuser":"' + reader.getValue("ftp_user") + '","ftppw":"' + reader.getValue("ftp_pw") + '","camhost":"' + reader.getValue("cam_host") + '","camdir":"' + reader.getValue("cam_dir") + '"}'
        return str(message)

    def sendLEDStatus(self):
        # Farbwerte aller einzelnen LEDs senden
        ledstatus = center.getLEDStatusAsJson()
        return ledstatus

    def changeConfiguration(self, config):
        b = config.split('--')
        key = b[0]
        value = b[1]
        center.changeConfiguration(key, value)
