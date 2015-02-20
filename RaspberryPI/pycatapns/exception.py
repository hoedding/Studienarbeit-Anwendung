'''

@author (C) 2013 Gerardo Ezquerra (catwashere@yahoo.com)
@file exception.py
@version 0.1

'''

class APNS_Exception(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)


class APNS_Message_Exception(APNS_Exception):
	def __init__(self, value):
		APNS_Exception.__init__(self, value)


class APNS_Push_Exception(APNS_Exception):
	def __init__(self, value):
		APNS_Exception.__init__(self, value)


class APNS_Push_Server_Exception(APNS_Push_Exception):
	def __init__(self, value):
		APNS_Push_Exception.__init__(self, value)