# Service Broker
import multiprocessing as mp

class ServiceBroker():
	def __init__(self):  # maybe pass as a param location of services?
		self._serviceRegistry = {}
		self._handlerRegistry = {}
		self._messageQueue = mp.Queue()  # docs claim its threadsafe
		self._handlerRegistry['useroutput'] = [self._userOutputHandler]


	def start(self):
		# threads for handling messages?
		# like spawn few threads to handle requests from different services
		while True:
			# handle some stuff
			return

	def _userOutputHandler(self, output: str):  # default handler
		print(output)

	def _loadServices(self): # method for loading the services from the folder
		# possibly add second one for refreshing
		return

	def _getHandler(self, name: str):
		try:
			return self._handlerRegistry[name][-1]
		except Exception:
			return None  # TODO log error
			# for the basic things it should never find empty key
			# unless the name itself does not exist
	
	def _addHandler(self, name: str, handler):
		try:
			self._handlerRegistry[name].append(handler)
		except Exception:
			return None  # TODO log error
			# errors when wrong name