#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting                          #
# Mail: mail[at]timohoeting.de                 #
################################################

import unittest
#from Server import *
#from Sensor import *
#from LED_Control import *
#from Center import *
from ConfigReader import *
import ConfigParser

class TestSequenceFunctions(unittest.TestCase):

    # Überprüfung aller Methoden, die auf die Reader-Klasse
    # zugreifen
    def test_getNumberOfLED(self):
        reader = ConfigReader()
        resultTest = reader.getNumberOfLED()
        config = ConfigParser.ConfigParser()
        config.read("./config.ini")
        resultCorrect = config.get("common", "number")
        self.assertEqual(resultTest, resultCorrect)

    def test_getHashPass(self):
        reader = ConfigReader()
        resultTest = reader.getHashPass()
        config = ConfigParser.ConfigParser()
        config.read("./config.ini")
        resultCorrect = config.get("common", "passhash")
        self.assertEqual(resultTest, resultCorrect)

    def test_getMotionPin1(self):
        reader = ConfigReader()
        resultTest = reader.getMotionPin1()
        config = ConfigParser.ConfigParser()
        config.read("./config.ini")
        resultCorrect = config.get("common", "motion1")
        self.assertEqual(resultTest, resultCorrect)

    def test_getMotionPin2(self):
        reader = ConfigReader()
        resultTest = reader.getMotionPin2()
        config = ConfigParser.ConfigParser()
        config.read("./config.ini")
        resultCorrect = config.get("common", "motion2")
        self.assertEqual(resultTest, resultCorrect)

    def test_camAvaible(self):
        reader = ConfigReader()
        resultTest = reader.camAvaible()
        config = ConfigParser.ConfigParser()
        config.read("./config.ini")
        resultCorrect = config.get("cam", "avaible")
        self.assertEqual(resultTest, resultCorrect)

    def test_camURL_MUST_FAIL(self):
        reader = ConfigReader()
        resultTest = reader.camURL()
        config = ConfigParser.ConfigParser()
        config.read("./config.ini")
        # Muss fehlschlagen!!!
        resultCorrect = '123' #config.get("cam","adress")
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

    def test_Status(self):
        import Status

    def test_LEDControl(self):
        import LED_Control

    def test_Effects(self):
        import Effects

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
    unittest.TextTestRunner(verbosity=2).run(suite)
