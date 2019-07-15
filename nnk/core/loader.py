import logging
import multiprocessing as mp
import importlib
from os import listdir
from os.path import isdir, isfile, join, abspath, dirname

from nnk.core.servicebroker import ServiceBroker
from nnk.utilities import threaded

lg = logging.getLogger('core.loader')


class Loader:
    def __init__(self, broker: ServiceBroker):
        self._sb = broker
        self._messageQueue = mp.Queue()
        self._moduleRegistry = {}
        self._sb.add_handler('loader', self._messageQueue)  # should register with broker as handler

    def get_queue(self) -> mp.Queue:
        return self._messageQueue

    @threaded(name='loader', daemon=True)
    def start(self):
        lg.info('starting')
        self._load_services()  # dbg only
        while True:
            msg = self._messageQueue.get()
            # TODO fill rest

    def stop(self):
        # kill all services
        for k, v in self._moduleRegistry.items():
            v['process'].kill()
            v['queue'].close()
            v['queue'].join_thread()

        self._messageQueue.close()
        self._messageQueue.join_thread()

    def start_service(self):
        raise Exception('not implemented')

    def stop_service(self, name: str):
        # should stop and remove it from internal registry of running services
        # so it wont be restarted during next keepalive (or maybe mark it as stopped
        # in the registry so it wont get reloaded
        if name in self._moduleRegistry:
            self._moduleRegistry[name]['process'].stop()
            self._moduleRegistry[name]['status'] = 'stopped'
        raise Exception('not implemented')

    def _load_services(self):
        # walk the modules dir, the directories names will be the services names
        # dynamically import folder+service.py file, build object with same name
        # and run start() on it, append to registry
        # run add_service on broker OR wait for the broker to ask for it or smth
        modules = [f for f in listdir(join(abspath(dirname(__file__)), '..', 'modules'))
                   if isdir(join(abspath(dirname(__file__)), '..', 'modules', f))]
        modules.remove('templatemodule')  # temporary(?) fix. templatemodule shouldnt be left in that foler later on

        loaded = 0
        for m in modules:
            if m not in self._moduleRegistry:
                module = importlib.import_module('.' + m + 'service', package='nnk.modules.' + m)
                service = getattr(module, m.capitalize() + 'Service')
                instance_queue = mp.Queue()
                instance = service(self._sb.get_queue(), instance_queue)
                process = mp.Process(target=instance.start, daemon=True)
                process.start()

                self._sb.add_service(m, instance_queue)
                self._moduleRegistry[m] = {'process': process, 'state': 'loaded', 'queue': instance_queue}

                lg.debug('started service: %s', m)
                loaded += 1
        if loaded == 1:
            lg.info('loaded 1 service')
        else:
            lg.info('loaded ', loaded, ' services')
    # should have looping keepalive method for loaded services

        # TODO add helper method get_state which would list all loaded services or specific ones

