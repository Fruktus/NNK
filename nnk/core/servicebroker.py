# Service Broker
import multiprocessing as mp
from . import configurator
from . import loader

class ServiceBroker():
	def __init__(self):  # maybe pass as a param location of services?
		# TODO figure out how to store the queues
		self._serviceRegistry = {}  # name of service -> dict: command name -> string? + something like empty -> queue
		self._handlerRegistry = {}  # name -> queue?
		self._messageQueue = mp.Queue()  # read by servicebroker, written by services # docs claim its threadsafe
		# TODO will most likely need queue for every service
		self._handlerRegistry['useroutput'] = [self._userOutputHandler]
		# service types:
		# user input
		# user output
		# service loader
		# config


	def start(self):
		# threads for handling messages?
		# like spawn few threads to handle requests from different services
		# can pass names to process
		self.process = mp.Process(target=self._start)  # TODO should or shouldn't be daemon?
		# self.process.daemon = True  # snippet
		self.process.start()

	def _start(self):
		# load and instantiate all other core components
		while True:
			# handle incoming messages
			msg = self._messageQueue.get()
			# TODO process message
			# raise Exception('not implemented')

	def stop(self):
		self.process.terminate()
		self.process.join()

	def _userOutputHandler(self, output: str):  # default handler
		print(output)

	def _loadServices(self): # method for loading the services from the folder
		# possibly add second one for refreshing
		return

	def _getHandler(self, name: str):
		try:
			return self._handlerRegistry[name][-1]
		except Exception:
			raise Exception('not implemented')  # TODO log error
			# for the basic things it should never find empty key
			# unless the name itself does not exist
	
	def _addHandler(self, name: str, handler):
		try:
			self._handlerRegistry[name].append(handler)
		except Exception:
			raise Exception('not implemented')  # TODO log error
			# errors when wrong name

	def _getService(self, name: str):
		raise Exception('not implemented')
	
	def _addService(self, name: str, service):
		raise Exception('not implemented')
