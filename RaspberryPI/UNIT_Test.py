#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting                          #
# Mail: mail[at]timohoeting.de                 #
################################################

import unittest
from ConfigReader import *
import json

class TestSequenceFunctions(unittest.TestCase):

    # Überprüfung aller Methoden, die auf die Reader-Klasse
    # zugreifen
    def test_getNumberOfLED(self):
        reader = ConfigReader()
        resultTest = reader.getNumberOfLED()
        data = open('config.json')
        jdata = json.load(data)
        resultCorrect = jdata["number"]
        self.assertEqual(resultTest, resultCorrect)

    def test_getHashPass(self):
        reader = ConfigReader()
        resultTest = reader.getHashPass()
        data = open('config.json')
        jdata = json.load(data)
        resultCorrect = jdata["passhash"]
        self.assertEqual(resultTest, resultCorrect)

    def test_getMotionPin1(self):
        reader = ConfigReader()
        resultTest = reader.getMotionPin1()
        data = open('config.json')
        jdata = json.load(data)
        resultCorrect = jdata["motion1"]
        self.assertEqual(resultTest, resultCorrect)

    def test_getMotionPin2(self):
        reader = ConfigReader()
        resultTest = reader.getMotionPin2()
        data = open('config.json')
        jdata = json.load(data)
        resultCorrect = jdata["motion2"]
        self.assertEqual(resultTest, resultCorrect)

    def test_camAvaible(self):
        reader = ConfigReader()
        resultTest = reader.camAvaible()
        data = open('config.json')
        jdata = json.load(data)
        resultCorrect = jdata["avaible"]
        self.assertEqual(resultTest, resultCorrect)

    def test_camURL_MUST_FAIL(self):
        reader = ConfigReader()
        resultTest = reader.camURL()
        # Muss fehlschlagen!!!
        resultCorrect = '123' #config.get("cam","adress")
        self.assertEqual(resultTest, resultCorrect)

    def test_getFTP(self):
        reader = ConfigReader()
        resultTest = reader.getFTP()
        data = open('config.json')
        jdata = json.load(data)
        resultCorrect = jdata["ftp"]
        self.assertEqual(resultTest, resultCorrect)

    def test_getToken(self):
        reader = ConfigReader()
        resultTest = reader.getToken()
        data = open('config.json')
        jdata = json.load(data)
        resultCorrect = jdata["token"]
        self.assertEqual(resultTest, resultCorrect)

    # Überprüfung ob alle Klassen ohne Fehler initialisiert
    # werden können
    def test_Center(self):
        import Center

    def test_Sensor(self):
        import Sensor

    def test_Sensor(self):
        import Sensor

    def test_Server(self):
        import Server

    def test_LEDControl(self):
        import LED_Control

    def test_ApplePush(self):
        import ApplePush

    # JSON Files auf korrekte Grammatik prüfen
    def test_Config(self):
        data = open('config.json')
        jdata = json.load(data)

    def test_Status(self):
        data = open('status.json')
        jdata = json.load(data)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
    unittest.TextTestRunner(verbosity=2).run(suite)
