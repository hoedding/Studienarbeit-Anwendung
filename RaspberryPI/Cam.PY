#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting                          #
# Mail: mail[at]timohoeting.de  			   #
################################################
import HTMLParser
import urllib2
import sys
from ConfigReader import *

class Cam():
    # Aktuell können Bilder aus dem HTML Kontext geladen werden
    # <img ... src="" ... </src>
    # Für endgültige Kamera muss das noch erweitert werden, da
    # vermutlich eine Authorisierung notwendig ist. Außerdem
    # ist es durchaus möglich, dass das Video nicht einfach als
    # Bild abreifbar ist.
    def getPicture(self):
        # URL der Cam einlesen
        reader = ConfigReader()
        url = reader.camURL()
        # Array mit allen Bildern
        global image
        image = []
        # Website abrufen mit HTTP-Request
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        encoding = response.headers.getparam('charset')
        page = response.read().decode(encoding)
        # HTML Parser starten
        parser = Parser()
        parser.feed(page)

        self.safeImage()

    def safeImage(self):
        # Alle Images im Array abspeichern
        # Cam1.jpg
        # Später soll nur noch ein Bild zurück gegeben werden,
        # damit es an den Server gesenet werden kann
        for i in range(len(image)):
            f = open('Cam'+str(i)+'.jpg', 'wb')
            f.write(image[i])
            f.close()

class Parser(HTMLParser.HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            img = Image()
            reader = ConfigReader()
            shorturl = reader.camShortURL()
            for name,value in attrs:
                if name == 'src':
                    image.append(img.getImage(shorturl + "/" + value))

class Image():
    def getImage(self,addr):
        u = urllib2.urlopen(addr)
        data = u.read()
        return data
