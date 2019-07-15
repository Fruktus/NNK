# Service Broker
import logging
import multiprocessing as mp
# from . import configurator
# from nnk.core.configurator import Configurator
# from nnk.core.loader import Loader
from nnk.messages import CommandMessage
from nnk.utilities import threaded

lg = logging.getLogger('core.broker')


class ServiceBroker:
	def __init__(self):  # maybe pass as a param location of services?
		# TODO figure out how to store the queues
		self._serviceRegistry = {}  # name of service -> queue
		self._handlerRegistry = {}  # name -> queue
		self._processorRegistry = {}  # handlername -> array of intermediate layers, should be interchangable
		self._messageQueue = mp.Queue()  # read by servicebroker, written by services # docs claim its threadsafe
		# TODO will most likely need queue for every service
		self._handlerRegistry['useroutput'] = [self._user_output_handler]
		# self.process = mp.Process(target=self._start)  # TODO should or shouldn't be daemon?
		# self.process.daemon = True  # snippet

		# service types:
		# user input
		# user output
		# service loader?
		# config

	@threaded(name='broker', daemon=True)
	def start(self):
		# threads for handling messages?
		# like spawn few threads to handle requests from different services
		# can pass names to process
		# self.process.start()  # runs _start in separate process

		lg.info('starting')
		# load and instantiate all other core components
		self._load_services()
		while True:
			# handle incoming messages
			msg = self._messageQueue.get()  # type: CommandMessage
			lg.debug(msg)
			# TODO handling should be in separate method
			# maybe instead of service getter make serviceSend
			# TODO check the type of message (isinstance)
			if msg.target in self._serviceRegistry:
				self._serviceRegistry[msg.target].put(msg)
			else:
				if msg.target in self._handlerRegistry:
					self.get_handler(msg.target).put(msg)  # FIXME
				else:
					lg.warning('no service nor handler found for name: \'%s\'', msg.target)

	def stop(self):
		# FIXME change to thread
		# the 'ugly' way, forcibly kills everything
		# TODO check if not possible to do more elegantly
		# can be done, use mp's events
		# self.process.terminate()
		# self.process.join()
		self._messageQueue.close()
		self._messageQueue.join_thread()

	def get_queue(self):
		return self._messageQueue

	def _user_output_handler(self, output: str):  # default handler
		print(output)

	def _load_services(self): # method for loading the services from the folder
		# FIXME since the loader became part of the core i can assume its always present as handler and not add it here
		# TODO decide whether i want to keep the object or not
		pass
		# ld = Loader()
		# lqueue = ld.get_queue()
		# ldr = mp.Process(target=ld.start)  # TODO should or shouldn't be daemon?
		# ldr.start()
		# self._add_handler('loader', lqueue)
		#
		# c = Configurator()
		# cqueue = c.getQueue()
		# cfg = mp.Process(target=c.start)  # TODO should or shouldn't be daemon?
		# cfg.start()
		# self._add_handler('config', cqueue)
		# self.process.daemon = True  # snippet

	def get_handler(self, name: str):
		if name in self._handlerRegistry:
			return self._handlerRegistry[name][-1]
		else:
			lg.error('handler not found: %s', name)
			# for the basic things it should never find empty key
			# unless the name itself does not exist

	# TODO should create method like process handle which would go through processors and pass to handler without getting
	# snippet for exactly that \/
	def pipeline_func(self, data, fns):
		"""takes data and array of functions to pipeline together"""
		from functools import reduce
		return reduce(lambda a, x: x(a), fns, data)
	
	def add_handler(self, name: str, handler: mp.Queue):
		if name not in self._handlerRegistry:
			self._handlerRegistry[name] = [handler]
		else:
			self._handlerRegistry[name].append(handler)
		lg.info('added handler: %s', name)

	def get_service(self, name: str):
		if name not in self._serviceRegistry:
			lg.error('service not found: %s', name)
			return
		return self._serviceRegistry[name]
	
	def add_service(self, name: str, service: mp.Queue):
		if name in self._serviceRegistry:
			lg.warning('readding existing service: %s', name)
		self._serviceRegistry[name] = service
		lg.debug('added service: %s', name)
