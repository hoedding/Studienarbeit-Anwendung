'''

@author (C) 2013 Gerardo Ezquerra (catwasandroid@gmail.com)
@file message.py
@version 0.1

'''

import re, sys
from json import JSONEncoder

from exception import APNS_Message_Exception

class APNS_Message:
	PAYLOAD_MAXIMUM_SIZE = 256
	
	DEVICE_TOKEN_LENGTH = 64

	APPLE_RESERVED_NAMESPACE = 'aps'
	INSIDE_APPLE_RESERVED_NAMESPACE = [
		'alert',
		'badge',
		'sound'
	]

	_bAutoAdjustLongPayload = True

	_aDeviceTokens = []

	_sText = None
	_nBadge = None
	_sSound = None

	_aCustomProperties = {}

	_nExpiryValue = 604800

	_mCustomIdentifier = None

	def __init__(self, sDeviceToken = None):
		self._bAutoAdjustLongPayload = True

		self._aDeviceTokens = []

		self._sText = None
		self._nBadge = None
		self._sSound = None

		self._aCustomProperties = {}

		self._nExpiryValue = 604800

		self._mCustomIdentifier = None
		if sDeviceToken != None:
			self.addRecipient(sDeviceToken)

	def addRecipient(self, sDeviceToken):
		matches = re.search('^[a-f0-9]{' + str(self.DEVICE_TOKEN_LENGTH) + '}', sDeviceToken)
		if matches == None or len(sDeviceToken) != self.DEVICE_TOKEN_LENGTH:
			raise APNS_Message_Exception(
				"Invalid device token '" + sDeviceToken + "'"
			)

		self._aDeviceTokens.append(sDeviceToken)

	def getRecipient(self, nRecipient = 0):
		if nRecipient < 0 or nRecipient >= len(self._aDeviceTokens):
			raise APNS_Message_Exception(
				"No recipient at index '" + str(nRecipient) + "'"
			);

		return self._aDeviceTokens[nRecipient]

	def getRecipientsNumber(self):
		return len(self._aDeviceTokens)

	def getRecipients(self):
		return self._aDeviceTokens

	def setText(self, sText):
		if not isinstance(sText, str):
			raise APNS_Message_Exception(
				"Invalid text string '" + str(sText) + "'"
			)
		self._sText = sText

	def getText(self):
		return self._sText

	def setBadge(self, nBadge):
		if not isinstance(nBadge, int):
			raise APNS_Message_Exception(
				"Invalid badge number '" + nBadge + "'"
			)
		self._nBadge = nBadge

	def getBadge(self):
		return self._nBadge

	def setSound(self, sSound = 'default'):
		if not isinstance(sSound, str):
			raise APNS_Message_Exception(
				"Invalid sound string '" + str(sSound) + "'"
			)
		self._sSound = sSound

	def getSound(self):
		return self._sSound

	def setCustomProperty(self, sName, mValue):
		if sName == self.APPLE_RESERVED_NAMESPACE:
			raise APNS_Message_Exception(
				"Property name '" + self.APPLE_RESERVED_NAMESPACE + "' can not be used for custom property."
			)
		self._aCustomProperties[sName.strip()] = mValue

	def getCustomPropertyNames(self):
		if not isinstance(self._aCustomProperties, dictionary):
			return []

		return self._aCustomProperties.keys()

	def getCustomProperty(self, sName):
		sName = sName.strip()

		if not sName in self._aCustomProperties:
			raise APNS_Message_Exception(
				"No property exists with the specified name '{" + sName + "}'."
			)

		return self._aCustomProperties[sName]

	def setAutoAdjustLongPayload(self, bAutoAdjust):
		self._bAutoAdjustLongPayload = bool(bAutoAdjust)

	def getAutoAdjustLongPayload(self):
		return self._bAutoAdjustLongPayload;

	def __str__(self):
		try:
			sJSONPayload = self.getPayload()
		except APNS_Message_Exception as e:
			sJSONPayload = ''

		return sJSONPayload

	def _getPayload(self):
		aPayload = {self.APPLE_RESERVED_NAMESPACE: {}}

		if self._sText != None and isinstance(self._sText, str):
			aPayload[self.APPLE_RESERVED_NAMESPACE]['alert'] = self._sText

		if self._nBadge != None and self._nBadge > 0:
			aPayload[self.APPLE_RESERVED_NAMESPACE]['badge'] = int(self._nBadge)
		
		if self._sSound != None and isinstance(self._sSound, str):
			aPayload[self.APPLE_RESERVED_NAMESPACE]['sound'] = self._sSound

		if len(self._aCustomProperties) > 0:
			aPayload.update(self._aCustomProperties)

		return aPayload

	def getPayload(self):
		sJSONPayload = JSONEncoder(separators=(',', ':')).encode(self._getPayload()).replace(
			'"' + self.APPLE_RESERVED_NAMESPACE + '":[]',
			'"' + self.APPLE_RESERVED_NAMESPACE + '":{}'
		)

		nJSONPayloadLen = len(sJSONPayload)

		if (nJSONPayloadLen > self.PAYLOAD_MAXIMUM_SIZE):
			if (self._bAutoAdjustLongPayload):
				nMaxTextLen = len(self._sText) - (nJSONPayloadLen - self.PAYLOAD_MAXIMUM_SIZE)
				if nMaxTextLen > 0:
					self._sText = self._sText[0:nMaxTextLen]
					return self.getPayload();
				else:
					raise APNS_Message_Exception(
						"JSON Payload is too long: " + str(nJSONPayloadLen) + " bytes. Maximum size is " +
						self.PAYLOAD_MAXIMUM_SIZE + " bytes. The message text can not be auto-adjusted."
					)
			else:
				raise APNS_Message_Exception(
					"JSON Payload is too long: " + str(nJSONPayloadLen) + " bytes. Maximum size is " +
					self.PAYLOAD_MAXIMUM_SIZE + " bytes"
				)

		return sJSONPayload

	def setExpiry(self, nExpiryValue):
		if not isinstance(nExpiryValue, int):
			raise APNS_Message_Exception(
				"Invalid seconds number '" + str(nExpiryValue) + "'"
			)

		self._nExpiryValue = nExpiryValue

	def getExpiry(self):
		return self._nExpiryValue

	def setCustomIdentifier(self, mCustomIdentifier):
		self._mCustomIdentifier = mCustomIdentifier

	def getCustomIdentifier(self):
		return self._mCustomIdentifier


class APNS_Message_Custom(APNS_Message):
	_sActionLocKey = None
	_sLocKey = None
	_aLocArgs = None
	_sLaunchImage = None

	def setActionLocKey(self, sActionLocKey = ''):
		self._sActionLocKey = sActionLocKey

	def getActionLocKey(self):
		return self._sActionLocKey

	def setLocKey(self, sLocKey):
		self._sLocKey = sLocKey

	def getLocKey(self):
		return self._sLocKey

	def setLocArgs(self, aLocArgs):
		self._aLocArgs = aLocArgs

	def getLocArgs(self):
		return self._aLocArgs

	def setLaunchImage(self, sLaunchImage):
		self._sLaunchImage = sLaunchImage

	def getLaunchImage(self):
		return self._sLaunchImage

	def _getPayload(self):
		aPayload = APNS_Message._getPayload(self)

		aPayload['aps']['alert'] = {}

		if self._sText != None and self._sText != "" and self._sLocKey == None:
			aPayload['aps']['alert']['body'] = self._sText

		if self._sActionLocKey != None and isinstance(self._sActionLocKey, str):
			if self._sActionLocKey == '':
				aPayload['aps']['alert']['action-loc-key'] = null
			else:
				aPayload['aps']['alert']['action-loc-key'] = self._sActionLocKey

		if self._sLocKey != None and isinstance(self._sLocKey, str):
			aPayload['aps']['alert']['loc-key'] = self._sLocKey

		if self._aLocArgs != None:
			aPayload['aps']['alert']['loc-args'] = self._aLocArgs

		if self._sLaunchImage != None and isinstance(self._sLaunchImage, str):
			aPayload['aps']['alert']['launch-image'] = self._sLaunchImage

		return aPayload;