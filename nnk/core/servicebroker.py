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
		# TODO implement command handling (adding, getting, removing, etc)
		self._commandsRegistry = {}  # name of service -> array of accepted keywords
		self._serviceRegistry = {}  # name of service -> queue
		self._handlerRegistry = {}  # name -> array of queues, only top one used, perhaps add priorities
		self._processorRegistry = {}  # handlername -> array of intermediate layers, should be interchangable

		self._messageQueue = mp.Queue()  # read by servicebroker, written by services # docs claim its threadsafe
		# TODO will most likely need queue for every service
		self._handlerRegistry['useroutput'] = [self._user_output_handler]
		# self.process = mp.Process(target=self._start)  # TODO should or shouldn't be daemon?
		#  broker possibly shouldn't to wait for other core threads
		# self.process.daemon = True  # snippet

	@threaded(name='broker', daemon=True)  # TODO most likely for removal, need to save the thread reference
	def start(self):
		# threads for handling messages?
		# like spawn few threads to handle requests from different services
		# can pass names to process
		# self.process.start()  # runs _start in separate process

		lg.info('starting')
		self._loop()

	def _loop(self):
		while True:
			# handle incoming messages
			msg = self._messageQueue.get()  # type: CommandMessage
			lg.debug(msg)
			# maybe instead of service getter make serviceSend
			# TODO check the type of message (isinstance) first
			if isinstance(msg, CommandMessage):
				self._handle_command(msg)

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

	# TODO perhaps replace with use_handler or smth
	def get_handler(self, name: str) -> mp.Queue:
		if name in self._handlerRegistry:
			return self._handlerRegistry[name][-1]
		else:
			lg.error('handler not found: %s', name)
			# for the basic things it should never find empty key
			# unless the name itself does not exist
	
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

	# TODO should create method like process handle which would go through processors and pass to handler without getting
	# snippet for exactly that \/
	def _pipeline_func(self, data, fns):
		"""takes data and array of functions to pipeline together"""
		# TODO: but that assumes all methods are static(?), whereas they require sending messaging all processors
		from functools import reduce
		return reduce(lambda a, x: x(a), fns, data)

	def _handle_command(self, cm: CommandMessage):
		# first check the command dict, if the entry is there, proceed
		module = cm.args[0]
		if module in self._commandsRegistry:
			if cm.args[1] in self._commandsRegistry[module]:
				self._serviceRegistry[module].put(cm)
			else:
				lg.warning('issued command not supported by module: ', cm.args[1])
		elif module in self._processorRegistry and module in self._handlerRegistry:
			pass
			# TODO the processor will most likely work on message in its loop,
			# TODO meaning that i'd need to keep track of how many processors completed its job
			# TODO on message to know which one use next
			# TODO is it possible that the module is in processors but not in handlers?
			# may not be here but still be in handlers

		elif module in self._handlerRegistry:
			self.get_handler(module).put(cm)
		else:
			lg.warning('requested module or handler not found: ', module)
