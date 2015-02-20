'''

@author (C) 2013 Gerardo Ezquerra (catwashere@yahoo.com)
@file feedback.py
@version 0.1

'''

import sys, select, math, binascii, struct

from datetime import datetime
from abstract import APNS_Abstract

PY_MAJOR_VERSION = sys.version_info[0]

class APNS_Feedback(APNS_Abstract):

	TIME_BINARY_SIZE = 4;
	TOKEN_LENGTH_BINARY_SIZE = 2;

	_aServiceURLs = [
		'ssl://feedback.push.apple.com:2196',
		'ssl://feedback.sandbox.push.apple.com:2196'
	]

	_aFeedback =[]

	def __init__(self, nEnvironment, sProviderCertificateFile):
		APNS_Abstract.__init__(self, nEnvironment, sProviderCertificateFile)

		self._aServiceURLs = [
			'ssl://feedback.push.apple.com:2196',
			'ssl://feedback.sandbox.push.apple.com:2196'
		]

		self._aFeedback =[]

	def receive(self):
		nFeedbackTupleLen = self.TIME_BINARY_SIZE + self.TOKEN_LENGTH_BINARY_SIZE + self.DEVICE_BINARY_SIZE;

		self._aFeedback =[]
		sBuffer = ""
		endOfFile = False
		try:
			while not endOfFile:
				self._log('INFO: Reading...')
				try:
					sCurrBuffer = self._hSocket.read(8192)

					sBuffer += sCurrBuffer
					nCurrBufferLen = len(sCurrBuffer)
					if nCurrBufferLen > 0:
						self._log("INFO: " + str(nCurrBufferLen) + " bytes read.");
					
					if nCurrBufferLen == 0:
						endOfFile = True

					del sCurrBuffer
					del nCurrBufferLen
				except:
					None

				nBufferLen = len(sBuffer);
				if nBufferLen >= nFeedbackTupleLen:
					nFeedbackTuples = int(math.floor(nBufferLen / nFeedbackTupleLen))
					for i in range(0, nFeedbackTuples):
						sFeedbackTuple = sBuffer[0:nFeedbackTupleLen]
						sBuffer = sBuffer[nFeedbackTupleLen:]
						aFeedback = self._parseBinaryTuple(sFeedbackTuple)
						self._aFeedback.append(aFeedback)

						
						date = datetime.fromtimestamp(aFeedback['timestamp'])
						buf = "INFO: New feedback tuple: timestamp=%d (%s), tokenLength=%d, deviceToken=%s." % (aFeedback['timestamp'], date.strftime("%Y-%m-%d %T"),
							aFeedback['tokenLength'], aFeedback['deviceToken'])
						self._log(buf)

						del aFeedback

				try:
					inputready = select.select([self._hSocket], [], [], (self._nSocketSelectTimeout/1000000.0))[0]
				except Exception as e:
					self._log('ERROR: Unable to wait for a stream availability.')
		except Exception as e:
			None

		return self._aFeedback;
	
	def _parseBinaryTuple(self, sBinaryTuple):
		apnsUnPackFormat = "!LH%ds" % (self.DEVICE_BINARY_SIZE)
		timestamp, tokenLength, deviceToken = struct.unpack_from(apnsUnPackFormat, sBinaryTuple)
		return {"timestamp":timestamp, "tokenLength":tokenLength, "deviceToken":binascii.hexlify(deviceToken)}
	
