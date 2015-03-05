#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting                          #
# Mail: mail[at]timohoeting.de  			   #
################################################
import sys
from ConfigReader import *
import ftplib

class Cam():
    #FTP Verzeichnis auslesen und alle gelisteten Dateinamen als
    # Array zurück geben
    def getPictureList(self):
        files = []
        reader = ConfigReader()
        if (reader.camAvaible() == "0"):
            return files
        ftphost = reader.getFTP()
        ftpdirectory = reader.getFTPDirectory()
        user = reader.getFTPUser()
        pw = reader.getFTPPW()
        ftp = ftplib.FTP(ftphost)
        try:
            if user == "" && pw == "":
                # Anonymous Login
                ftp.login()
            else:
                ftp.login(user,pw)
        except:
            return files
        ftp.cwd(ftpdirectory)
        files = ftp.nlst()
        ftp.quit()
        return files
