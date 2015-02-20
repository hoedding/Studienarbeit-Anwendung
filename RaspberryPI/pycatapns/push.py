'''

@author (C) 2013 Gerardo Ezquerra (catwashere@yahoo.com)
@file push.py
@version 0.1

'''

import sys, binascii, time, struct, select, copy, signal

from abstract import APNS_Abstract
from exception import APNS_Push_Exception
from message import APNS_Message

PY_MAJOR_VERSION = sys.version_info[0]

class APNS_Push(APNS_Abstract):
	COMMAND_PUSH = 1

	ERROR_RESPONSE_SIZE = 6
	ERROR_RESPONSE_COMMAND = 8

	STATUS_CODE_INTERNAL_ERROR = 999

	_aErrorResponseMessages = {}

	_nSendRetryTimes = 3

	_aServiceURLs = []

	_aMessageQueue = {}
	_aErrors = {}

	def __init__(self, nEnvironment, sProviderCertificateFile):
		APNS_Abstract.__init__(self, nEnvironment, sProviderCertificateFile)

		self._aErrorResponseMessages = {
			0: 'No errors encountered',
			1: 'Processing error',
			2: 'Missing device token',
			3: 'Missing topic',
			4: 'Missing payload',
			5: 'Invalid token size',
			6: 'Invalid topic size',
			7: 'Invalid payload size',
			8: 'Invalid token',
			self.STATUS_CODE_INTERNAL_ERROR: 'Internal error'
		}

		self._nSendRetryTimes = 3

		self._aServiceURLs = [
			'ssl://gateway.push.apple.com:2195',
			'ssl://gateway.sandbox.push.apple.com:2195'
		]

		self._aMessageQueue = {}
		self._aErrors = {}

	def setSendRetryTimes(self, nRetryTimes):
		self._nSendRetryTimes = int(nRetryTimes)

	def getSendRetryTimes(self):
		return self._nSendRetryTimes
	
	def add(self, message):
		if not isinstance(message, APNS_Message):
			raise APNS_Push_Exception(
				"Unable to use an instance of '" + message.__class__.__name__ + "' as message: " +
				"a message must implements APNS_Message."
			)

		sMessagePayload = message.getPayload()
		nRecipients = message.getRecipientsNumber()

		nMessageQueueLen = len(self._aMessageQueue)
		for i in range(0, nRecipients):
			nMessageID = nMessageQueueLen + i + 1
			self._aMessageQueue[nMessageID] = {
				'MESSAGE': message,
				'BINARY_NOTIFICATION': self._getBinaryNotification(
					message.getRecipient(i),
					sMessagePayload,
					nMessageID,
					message.getExpiry()
				),
				'ERRORS': []
			}

	def send(self):
		if not self._hSocket:
			raise APNS_Push_Exception(
				'Not connected to Push Notification Service'
			)

		if len(self._aMessageQueue) == 0:
			raise APNS_Push_Exception(
				'No notifications queued to be sent'
			)

		self._aErrors = {}
		
		nRun = 1
		while len(self._aMessageQueue) > 0:

			nMessages = len(self._aMessageQueue)
			self._log("INFO: Sending messages queue, run #" + str(nRun) + ": " + str(nMessages) + " message(s) left in queue.")

			bError = False

			dataCopy = copy.deepcopy(self._aMessageQueue)
			for k in dataCopy:
				#dispatch signals if has to
				
				aMessage = self._aMessageQueue[k]
				message = aMessage['MESSAGE']

				val = "unset"
				sCustomIdentifier = message.getCustomIdentifier()
				if sCustomIdentifier != None and sCustomIdentifier != "":
					val = sCustomIdentifier

				sCustomIdentifier = '[custom identifier: %s]' % (val)

				nErrors = 0
				mRemoved = False
				if len(aMessage['ERRORS']) != 0:
					for aError in aMessage['ERRORS']:
						if aError['statusCode'] == 0:
							self._log("INFO: Message ID " + str(k) + " " + str(sCustomIdentifier) + " has no error (" + str(aError['statusCode']) + "), removing from queue...")
							self._removeMessageFromQueue(k)
							mRemoved = True
						elif aError['statusCode'] > 1 and aError['statusCode'] <= 8:
							self._log("WARNING: Message ID " + str(k) + " " + str(sCustomIdentifier) + " has an unrecoverable error (" + str(aError['statusCode']) + "), removing from queue without retrying...")
							self._removeMessageFromQueue(k, True)
							mRemoved = True
					if len(aMessage['ERRORS']) >= self._nSendRetryTimes:
						nErrors = len(aMessage['ERRORS'])
						self._log(
							"WARNING: Message ID " + str(k) + " " + str(sCustomIdentifier) + " has " + str(nErrors) + " errors, removing from queue..."
						)
						self._removeMessageFromQueue(k, True)
						mRemoved = True

				if not mRemoved:
					nLen = len(aMessage['BINARY_NOTIFICATION'])
					self._log("STATUS: Sending message ID " + str(k) + " " + sCustomIdentifier + " (" + str(nErrors + 1) + "/" + str(self._nSendRetryTimes) + "): " + str(nLen) + " bytes.")

					aErrorMessage = None
					try:
						nWritten = self._hSocket.send(aMessage['BINARY_NOTIFICATION'])
					except:
						nWritten = 0
					
					if nLen != nWritten:
						buf = '%s (%d bytes written instead of %d bytes)' % (self._aErrorResponseMessages[self.STATUS_CODE_INTERNAL_ERROR], nWritten, nLen)
						aErrorMessage = {
							'identifier': k,
							'statusCode': self.STATUS_CODE_INTERNAL_ERROR,
							'statusMessage': buf
						}
					time.sleep(self._nWriteInterval/1000000.0)

					bError = self._updateQueue(aErrorMessage)
					if bError:
						break

			if not bError:
				try:
					inputready = select.select([self._hSocket], [], [], (self._nSocketSelectTimeout/1000000.0))[0]
					if len(inputready) == 0:
						self._aMessageQueue = {}
						break
					elif len(inputready) > 0:
						bError = self._updateQueue()
						if not bError:
							self._aMessageQueue = {}
					else:
						self._log('ERROR: Unable to wait for a stream availability.')
				except Exception as e:
					self._log('ERROR: Unable to wait for a stream availability.')
					self._aMessageQueue = {}

			nRun += 1

	def getQueue(self, bEmpty = True):
		aRet = self._aMessageQueue
		if bEmpty:
			self._aMessageQueue = {}
		return aRet

	def getErrors(self, bEmpty = True):
		aRet = self._aErrors
		if bEmpty:
			self._aErrors = {}
		return aRet

	def _getBinaryNotification(self, sDeviceToken, sPayload, nMessageID = 0, nExpire = 604800):
		nPayloadLength = len(sPayload)

		if nExpire > 0:
			nExpire += time.time()

		apnsPackFormat = "!BIIH%dsH%ds" % (self.DEVICE_BINARY_SIZE, nPayloadLength)
		if PY_MAJOR_VERSION > 2:
			packet = struct.pack(apnsPackFormat, 
				int(self.COMMAND_PUSH), 
				int(nMessageID),
				int(nExpire),
				self.DEVICE_BINARY_SIZE, 
				binascii.unhexlify(sDeviceToken), 
				nPayloadLength, 
				bytearray(sPayload, encoding='ascii'))
		else:
			packet = struct.pack(apnsPackFormat, 
				int(self.COMMAND_PUSH), 
				int(nMessageID),
				int(nExpire),
				self.DEVICE_BINARY_SIZE, 
				binascii.unhexlify(sDeviceToken), 
				nPayloadLength, 
				sPayload)
		
		return packet
	
	def _parseErrorMessage(self, sErrorMessage):
		command, statusCode, identifier = struct.unpack_from('!BBL', sErrorMessage)
		return {"command":command, "statusCode":statusCode, "identifier":identifier}
	
	def _readErrorMessage(self):
		try:
			sErrorResponse = self._hSocket.recv(self.ERROR_RESPONSE_SIZE)
			
			if sErrorResponse == False or len(sErrorResponse) != self.ERROR_RESPONSE_SIZE:
				return
			
			aErrorResponse = self._parseErrorMessage(sErrorResponse)
			
			if (not isinstance(aErrorResponse, dict)) or aErrorResponse == None or len(aErrorResponse) == 0:
				return
			
			if aErrorResponse['command'] == None or aErrorResponse['statusCode'] == None or aErrorResponse['identifier'] == None:
				return

			if aErrorResponse['command'] != self.ERROR_RESPONSE_COMMAND:
				return
			
			aErrorResponse['time'] = time.time()
			aErrorResponse['statusMessage'] = 'None (unknown)'
			if aErrorResponse['statusCode'] in self._aErrorResponseMessages:
				aErrorResponse['statusMessage'] = self._aErrorResponseMessages[aErrorResponse['statusCode']]

			return aErrorResponse
		except:
			return

	def _updateQueue(self, aErrorMessage = None):
		aStreamErrorMessage = self._readErrorMessage()
		if aErrorMessage == None and aStreamErrorMessage == None:
			return False
		elif aErrorMessage != None and aStreamErrorMessage != None:
			if aStreamErrorMessage['identifier'] <= aErrorMessage['identifier']:
				aErrorMessage = aStreamErrorMessage
				del aStreamErrorMessage
		elif aErrorMessage == None and aStreamErrorMessage != None:
			aErrorMessage = aStreamErrorMessage
			del aStreamErrorMessage

		self._log('ERROR: Unable to send message ID ' +
			str(aErrorMessage['identifier']) + ': ' +
			aErrorMessage['statusMessage'] + ' (' + str(aErrorMessage['statusCode']) + ').')

		self.disconnect()

		self._aMessageQueue = {key: value for key, value in self._aMessageQueue.items() if key >= aErrorMessage['identifier']}
		for k in self._aMessageQueue.keys():
			if k == aErrorMessage['identifier']:
				self._aMessageQueue[k]['ERRORS'].append(aErrorMessage)
			else:
				break

		self.connect()

		return True
	
	def _removeMessageFromQueue(self, nMessageID, bError = False):
		if (not isinstance(nMessageID, int)) or nMessageID <= 0:
			raise APNS_Push_Exception(
				'Message ID format is not valid.'
			)

		if not nMessageID in self._aMessageQueue:
			raise APNS_Push_Exception(
				"The Message ID {$nMessageID} does not exists."
			)

		if bError:
			self._aErrors[nMessageID] = self._aMessageQueue[nMessageID]

		del self._aMessageQueue[nMessageID]


