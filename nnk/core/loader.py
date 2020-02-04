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
        self._moduleRegistry = {}  # dict of process name, its state and its message queue
        # TODO perhaps use registration message instead
        self._sb.add_handler('loader', self._messageQueue)  # should register with broker as handler
        # TODO should also register as a service(?) and expose commands (like start/stop service etc)

    def get_queue(self) -> mp.Queue:
        return self._messageQueue

    @threaded(name='loader', daemon=True)
    def start(self):
        lg.info('starting')
        self._load_services()  # dbg only(?)
        while True:
            msg = self._messageQueue.get()
            # TODO add handling messages

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
        modules.remove('templatemodule')  # FIXME temporary fix. templatemodule will be moved elsewhere later on
        if '__pycache__' in modules:
            modules.remove('__pycache__')  # FIXME temporary, figure out better way to filter the folder

        # TODO keep track of all modules that were present in folder, how many were loaded etc.
        # TODO it is required for discovering dynamically added modules
        loaded = 0
        for m in modules:
            if m not in self._moduleRegistry:
                module = importlib.import_module('.' + m + 'service', package='nnk.modules.' + m)
                service = getattr(module, m.capitalize() + 'Service')
                instance_queue = mp.Queue()
                instance = service(self._sb.get_queue(), instance_queue)
                process = mp.Process(target=instance.start, daemon=True)
                process.start()

                # FIXME new modules should probably register by themselves with broker
                self._sb.add_service(m, instance_queue)
                # TODO replace state with string constants
                self._moduleRegistry[m] = {'process': process, 'state': 'loaded', 'queue': instance_queue}

                lg.debug('started service: %s', m)
                loaded += 1
        if loaded == 1:
            lg.info('loaded 1 service')
        else:
            lg.info('loaded {0} services'.format(loaded))
        # TODO from importlib doc:
        # If you are dynamically importing a module that was created since the interpreter began execution
        # (e.g., created a Python source file), you may need to call invalidate_caches() in order for the new module to
        # be noticed by the import system.

    # should have looping keepalive method for loaded services, there is a snippet for that in nnk.md

        # TODO add helper method get_state which would list all loaded services or specific ones

