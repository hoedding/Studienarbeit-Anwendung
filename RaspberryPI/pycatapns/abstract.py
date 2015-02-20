'''

@author (C) 2013 Gerardo Ezquerra (catwashere@yahoo.com)
@file abstract.py
@version 0.1

'''

import os, stat, sys, socket, ssl, asyncore
from time import sleep

PY_MAJOR_VERSION = sys.version_info[0]
if PY_MAJOR_VERSION > 2:
	from urllib.parse import urlparse
else:
	from urlparse import urlparse

from exception import APNS_Exception
from log import APNS_Log_Embedded, APNS_Log_Interface

class APNS_Abstract():
	ENVIRONMENT_PRODUCTION = 0
	ENVIRONMENT_SANDBOX = 1

	CERTS_PATH = "certs/"

	DEVICE_BINARY_SIZE = 32

	DEFAULT_TIME_OUT_CONNECTION = 15

	WRITE_INTERVAL = 10000
	CONNECT_RETRY_INTERVAL = 1000000
	SOCKET_SELECT_TIMEOUT = 1000000

	_aServiceURLs = []

	_nEnvironment = None

	_nConnectTimeout = None
	_nConnectRetryTimes = 3

	_sProviderCertificateFile = None
	_sRootCertificationAuthorityFile = None

	_nWriteInterval = None
	_nConnectRetryInterval = None
	_nSocketSelectTimeout = None

	_logger = None

	_hSocket = None
	_rSocket = None

	def __init__(self, nEnvironment, sProviderCertificateFile):
		self._aServiceURLs = []

		self._nEnvironment = None

		self._nConnectTimeout = None
		self._nConnectRetryTimes = 3

		self._sProviderCertificateFile = None
		self._sRootCertificationAuthorityFile = None

		self._nConnectRetryInterval = None
		self._nSocketSelectTimeout = None

		self._logger = None

		self._hSocket = None
		self._rSocket = None

		if nEnvironment != self.ENVIRONMENT_PRODUCTION and nEnvironment != self.ENVIRONMENT_SANDBOX:
			raise APNS_Exception(
				"Invalid environment '" + str(nEnvironment) + "'"
			)

		self._nEnvironment = nEnvironment

		if not self.__is_readable(self.CERTS_PATH + sProviderCertificateFile):
			raise APNS_Exception(
				"Unable to read certificate file '" + self.CERTS_PATH + sProviderCertificateFile + "'"
			)

		self._sProviderCertificateFile = self.CERTS_PATH + sProviderCertificateFile

		self._nConnectTimeout = self.DEFAULT_TIME_OUT_CONNECTION
		self._nWriteInterval = self.WRITE_INTERVAL
		self._nConnectRetryInterval = self.CONNECT_RETRY_INTERVAL
		self._nSocketSelectTimeout = self.SOCKET_SELECT_TIMEOUT

	def __is_readable(self, path):
		uid = os.getuid()
		euid = os.geteuid()
		gid = os.getgid()
		egid = os.getegid()

		if uid == euid and gid == egid:
			return os.access(path, os.R_OK)

		st = os.stat(path)

		if st.st_uid == euid:
			return st.st_mode & stat.S_IRUSR != 0

		groups = os.getgroups()
		if st.st_gid == egid or st.st_gid in groups:
			return st.st_mode & stat.S_IRGRP != 0

		return st.st_mode & stat.S_IROTH != 0

	def setLogger(self, logger):
		if not isinstance(logger, APNS_Log_Interface):
			raise APNS_Exception(
				"Unable to use an instance of '" + logger.__class__.__name__ + "' as logger: " +
				"a logger must implements APNS_Log_Interface."
			)

		self._logger = logger

	def getLogger(self):
		return self._logger

	def setRootCertificationAuthority(self, sRootCertificationAuthorityFile):
		if not self.__is_readable(self.CERTS_PATH + sRootCertificationAuthorityFile):
			raise APNS_Exception(
				"Unable to read Certificate Authority file '" + self.CERTS_PATH + sRootCertificationAuthorityFile+ "'"
			)

		self._sRootCertificationAuthorityFile = self.CERTS_PATH + sRootCertificationAuthorityFile

	def getCertificateAuthority(self):
		return self._sRootCertificationAuthorityFile

	def setWriteInterval(self, nWriteInterval):
		self._nWriteInterval = int(nWriteInterval)

	def getWriteInterval(self):
		return self._nWriteInterval

	def setConnectTimeout(self, nTimeout):
		self._nConnectTimeout = int(nTimeout)

	def getConnectTimeout(self):
		return self._nConnectTimeout

	def setConnectRetryTimes(self, nRetryTimes):
		self._nConnectRetryTimes = int(nRetryTimes)

	def getConnectRetryTimes(self):
		return self._nConnectRetryTimes

	def setConnectRetryInterval(self, nRetryInterval):
		self._nConnectRetryInterval = int(nRetryInterval)

	def getConnectRetryInterval(self):
		return self._nConnectRetryInterval

	def setSocketSelectTimeout(self, nSelectTimeout):
		self._nSocketSelectTimeout = int(nSelectTimeout)

	def getSocketSelectTimeout(self):
		return self._nSocketSelectTimeout

	def connect(self):
		bConnected = False
		nRetry = 0
		while not bConnected:
			try:
				bConnected = self._connect()
			except APNS_Exception as e:
				if nRetry >= self._nConnectRetryTimes:
					raise e
				else:
					self._log('ERROR: ' + str(e))
					self._log(
						"INFO: Retry to connect (" + str(nRetry+1) +
						"/" + str(self._nConnectRetryTimes) + ")..."
					)
					sleep(self._nConnectRetryInterval/1000000.0)

			nRetry += 1

	def disconnect(self):
		if self._hSocket:
			self._log('INFO: Disconnected.')
			return self._hSocket.close()
		return False

	def _connect(self):
		sURL = self._aServiceURLs[self._nEnvironment]
		#del aURLs

		self._log("INFO: Trying " + sURL + "...")

		self._rSocket = socket.socket()

		self._rSocket.settimeout(self._nConnectTimeout)

		self._hSocket = ssl.wrap_socket(
			self._rSocket,
			ssl_version = ssl.PROTOCOL_TLSv1,
			ca_certs = self._sRootCertificationAuthorityFile,
			certfile = self._sProviderCertificateFile,
			cert_reqs = ssl.CERT_REQUIRED
		)

		url = urlparse(sURL)
		if url.port == None:
			url.port = 80

		apns_address = (url.geturl().replace(":" + str(url.port), "").replace(url.scheme + "://", ""), int(url.port))

		sError = None

		try:
			self._hSocket.connect(apns_address)
		except socket.error as e:
			sError = e

		if not self._hSocket or sError != None:
			raise APNS_Exception(
				"Unable to connect to '" + sURL + "': " + str(sError)
			)

		self._hSocket.settimeout(None)
		self._hSocket.setblocking(False)
		#stream_set_write_buffer(self._hSocket, 0)

		self._log("INFO: Connected to " + sURL + ".")

		return True

	def _log(self, sMessage):
		if not self._logger:
			self._logger = APNS_Log_Embedded()
		self._logger.log(sMessage)
