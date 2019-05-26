# Service Broker
import multiprocessing as mp
# from . import configurator
from nnk.core.configurator import Configurator
from nnk.core.loader import Loader
from nnk.message import Message

class ServiceBroker():
	def __init__(self):  # maybe pass as a param location of services?
		# TODO figure out how to store the queues
		self._serviceRegistry = {}  # name of service -> queue
		self._handlerRegistry = {}  # name -> queue
		self._messageQueue = mp.Queue()  # read by servicebroker, written by services # docs claim its threadsafe
		# TODO will most likely need queue for every service
		self._handlerRegistry['useroutput'] = [self._userOutputHandler]
		# service types:
		# user input
		# user output
		# service loader?
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
		self._loadServices()
		while True:
			# handle incoming messages
			msg = self._messageQueue.get()  # type: Message

			# TODO possibly should be in separate method
			# maybe instead of service getter make serviceSend
			# TODO definitely use separate method
			try:
				self._serviceRegistry[msg.target].put(msg)
			except Exception:
				try:
					self._handlerRegistry[msg.target].put(msg)
				except Exception:
					# FIXME temporary
					raise Exception('no service nor handler found')

	def stop(self):
		# the 'ugly' way, forcibly kills everything
		# TODO check if not possible to do more elegantly
		# can be done, use mp's events
		self.process.terminate()
		self.process.join()

	def _userOutputHandler(self, output: str):  # default handler
		print(output)

	def _loadServices(self): # method for loading the services from the folder
		# TODO decide whether i want to keep the object or not
		ld = Loader()
		lqueue = ld.getQueue()
		ldr = mp.Process(target=ld.start)  # TODO should or shouldn't be daemon?
		ldr.start()
		self._addHandler('loader', lqueue)

		c = Configurator()
		cqueue = c.getQueue()
		cfg = mp.Process(target=c.start)  # TODO should or shouldn't be daemon?
		cfg.start()
		self._addHandler('config', cqueue)
		# self.process.daemon = True  # snippet

	def _getHandler(self, name: str):
		try:
			return self._handlerRegistry[name][-1]
		except Exception:
			raise Exception('not implemented')  # TODO log error
			# for the basic things it should never find empty key
			# unless the name itself does not exist
	
	def _addHandler(self, name: str, handler: mp.Queue):
		try:
			self._handlerRegistry[name].append(handler)
		except Exception:
			raise Exception('not implemented')  # TODO log error
			# errors when wrong name

	def _getService(self, name: str):
		raise Exception('not implemented')
	
	def _addService(self, name: str, service: mp.Queue):
		raise Exception('not implemented')
