import multiprocessing as mp

from nnk.core.servicebroker import ServiceBroker


class Loader:
    def __init__(self, broker: ServiceBroker):
        self._sb = broker
        self._messageQueue = mp.Queue()
        # should register with broker as handler
        raise Exception('not implemented')

    def get_queue(self) -> mp.Queue:
        return self._messageQueue

    def start(self):
        raise Exception('not implemented')

    def start_service(self):
        raise Exception('not implemented')

    def stop_service(self):
        # should stop and remove it from internal registry of running services
        # so it wont be restarted during next keepalive (or maybe mark it as stopped
        # in the registry so it wont get reloaded
        raise Exception('not implemented')

    def _load_services(self):
        # walk the modules dir, the directories names will be the services names
        # dynamically import folder+service.py file, build object with same name
        # and run start() on it, append to registry
        # run add_service on broker OR wait for the broker to ask for it or smth
        raise Exception('not implemented')

    # should have looping keepalive method for loaded services
