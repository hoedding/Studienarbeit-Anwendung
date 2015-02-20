'''

@author (C) 2013 Gerardo Ezquerra (catwashere@yahoo.com)
@file log.py
@version 0.1

'''

import os

from datetime import date

class APNS_Log_Interface: 
	def log(self, sMessage):
		print(sMessage)

class APNS_Log_Embedded(APNS_Log_Interface): 
	def log(self, sMessage):
		today = date.today()
		buf = "%s APNS[%d]: %s" % (today.strftime("%x"), os.getpid(), sMessage.strip())
		print(buf)