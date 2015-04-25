#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting                          #
# Mail: mail[at]timohoeting.de                 #
################################################

from ConfigWriter import *

class setup():
    def run(self):
        print '############# Konfiguration gestartet  ##############'
        self.raspberryConfig()
        self.camConfig()

    def raspberryConfig(self):
        writer = ConfigWriter()
        print '##########    Konfiguration Raspberry Pi  ###########'
        print '#######  Benutzer: admin                     ########'
        print '#######  Passwort: password                  ########'
        ledport = raw_input("Port der LED? ")
        ledcount = raw_input("Anzahl der angeschlossenen LEDs? ")
        motionport1 = raw_input("Port Bewegungssensor 1? ")
        motionport2 = raw_input("Port Bewegungssensor 2? ")
        timer  = raw_input("Zeitdauer bei Bewegungsmelder? ")
        writer.changeConfig("username", "armin")
        writer.changeConfig("pw", "d63dc919e201d7bc4c825630d2cf25fdc93d4b2f0d46706d29038d01")
        writer.changeConfig("ledport", ledport)
        writer.changeConfig("ledcount", ledcount)
        writer.changeConfig("motionport1", motionport1)
        writer.changeConfig("motionport2", motionport2)
        writer.changeConfig("timerperiod", timer)

    def camConfig(self):
        writer = ConfigWriter()
        print '##########  Konfiguration Netzwerkkamera  ###########'
        camavaible = raw_input("Netzwerkkamera verfügbar? y/n ")
        cam = False
        if (camavaible == "y"):
            cam = True
        if (cam == False):
            writer.changeConfig("camavaible", "0")
            return
        cam_host = raw_input("Adresse der Netzwerkkamera? ")
        cam_dir = raw_input("Verzeichnis der Netzwerkkamera? Für HTTP-Request. ")
        cam_user = raw_input("Benutzer der Netzwerkkamera? ")
        cam_pw = raw_input("Passwort der Netzwerkkamera? ")
        writer.changeConfig("camavaible", "1")
        writer.changeConfig("cam_host",cam_host)
        writer.changeConfig("cam_dir",cam_dir)
        writer.changeConfig("cam_user",cam_user)
        writer.changeConfig("cam_pw",cam_pw)
        self.ftpConfig()

    def ftpConfig(self):
        writer = ConfigWriter()
        print '##########  Konfiguration FTP-Server      ###########'
        ftp_host = raw_input("Adresse FTP-Server? ")
        ftp_directory = raw_input("FTP-Verzeichnis? ")
        ftp_user = raw_input("Benutzer FTP-Server? ")
        ftp_pw = raw_input("Passwort FTP-Server? ")
        writer.changeConfig("ftp_host",ftp_host)
        writer.changeConfig("ftp_directory",ftp_directory)
        writer.changeConfig("ftp_user",ftp_user)
        writer.changeConfig("ftp_pw",ftp_pw)
        print '# Konfiguration beendet.                            #'
        print '#####################################################'

if __name__ == "__main__":
    setup = setup()
    setup.run()
