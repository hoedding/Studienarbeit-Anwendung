'''

@author (C) 2013 Gerardo Ezquerra (catwashere@yahoo.com)
@file server.py
@version 0.1

'''

import os, signal, atexit, copy

from time import sleep
from multiprocessing import Queue
from push import APNS_Push
from exception import APNS_Push_Server_Exception
from message import APNS_Message


class APNS_Push_Server(APNS_Push):
	MAIN_LOOP_USLEEP = 200000
	QUEUE_TIMEOUT = 1000000

	_nProcesses = 3

	_nParentPid = 0
	_nCurrentProcess = 0
	_nRunningProcesses = 0
	_bAlive = True

	_hQueue = None
	_hErrors = None

	_aErrors = []

	def __init__(self, nEnvironment, sProviderCertificateFile):
		APNS_Push.__init__(self, nEnvironment, sProviderCertificateFile)

		self._nProcesses = 3
	
		self._nParentPid = 0
		self._nCurrentProcess = 0
		self._nRunningProcesses = 0

		self._hQueue = None
		self._hErrors = None
		self._aErrors = []

		self._nParentPid = os.getpid()
		self._bAlive = True

		atexit.register(self.onShutdown)

		signal.signal(signal.SIGCHLD, self.onChildExited)
		for nSignal in [signal.SIGTERM, signal.SIGQUIT, signal.SIGINT]:
			signal.signal(nSignal, self.onSignal)

		if os.getpid() == self._nParentPid:
			self._hQueue = Queue()
			self._hErrors = Queue()

	def run(self):
		#dispatch signals if has to
		return self._nRunningProcesses > 0

	def onChildExited(self, nSignal, frame):
		pid, status = os.waitpid(-1, os.WNOHANG)
		while pid > 0:
			self._nRunningProcesses -= 1
			try: 
				pid, status = os.waitpid(-1, os.WNOHANG)
			except:
				pid = 0

	def onSignal(self, nSignal, frame):
		if nSignal == signal.SIGTERM or nSignal == signal.SIGQUIT or nSignal == signal.SIGINT:
			nPid = os.getpid()
			if nPid != self._nParentPid:
				self._log("INFO: Child " + str(nPid) + " received signal #" + str(nSignal) + ", shutdown...")
				self._bAlive = False
		else:
			self._log("INFO: Ignored signal #" + str(nSignal) + ".")

	def onShutdown(self):
		if os.getpid() == self._nParentPid:
			self._log('INFO: Parent shutdown, cleaning memory...')

	def setProcesses(self, nProcesses):
		nProcesses = int(nProcesses)
		if nProcesses <= 0:
			return
		self._nProcesses = nProcesses

	def start(self):
		for i in range(0, self._nProcesses):
			self._nCurrentProcess = i
			nPid = os.fork()
			if nPid == -1:
				self._log('WARNING: Could not fork')
			elif nPid > 0:
				#parent process
				self._log("INFO: Forked process PID " + str(nPid))
				self._nRunningProcesses += 1
			else:
				#child process
				try:
					APNS_Push.connect(self)
				except ApnsPHP_Exception as e:
					self._log('ERROR: ' + e + ', exiting...')
					exit(1)

				self._mainLoop()
				APNS_Push.disconnect(self)
				exit(0)

	def add(self, message):
		if not isinstance(message, APNS_Message):
			raise APNS_Push_Server_Exception(
				"Unable to use an instance of '" + message.__class__.__name__ + "' as message: " +
				"a message must implements APNS_Message."
			)

		self._hQueue.put(message)

	def getQueue(self, bEmpty = True):
		aQueue = []
		if not bEmpty:
			hQueue = Queue()

		while not self._hQueue.empty():
			try:
				data = self._hQueue.get(True, self.QUEUE_TIMEOUT / 1000000.0)
				aQueue.append(data)
				if not bEmpty:
					hQueue.put(data)
			except:
				None

		if not bEmpty:
			self._hQueue = hQueue

		return aQueue

	def getErrors(self, bEmpty = True):
		if bEmpty:
			self._aErrors = []

		while not self._hErrors.empty():
			try:
				data = self._hErrors.get(True, self.QUEUE_TIMEOUT / 1000000.0)
				self._aErrors.append(data)
			except:
				None

		return copy.deepcopy(self._aErrors)

	def _mainLoop(self):
		while self._bAlive:

			if os.getppid() != self._nParentPid:
				self._log("INFO: Parent process " + str(self._nParentPid) + " died unexpectedly, exiting...")
				break

			errors = APNS_Push.getErrors(self)
			if isinstance(errors, dict) and len(errors) > 0:
				for k, error in errors.items():
					self._hErrors.put(error)

			try:
				message = self._hQueue.get(True, self.QUEUE_TIMEOUT / 1000000.0)
				APNS_Push.add(self, message)
				nMessages = 1
			except:
				nMessages = 0
				
			if nMessages > 0:
				self._log('INFO: Process ' + str(self._nCurrentProcess + 1) + " has " + str(nMessages) + " messages, sending...")
				APNS_Push.send(self)
			else:
				sleep(self.MAIN_LOOP_USLEEP / 1000000.0)
