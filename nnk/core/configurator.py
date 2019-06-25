import multiprocessing as mp

from nnk.core.servicebroker import ServiceBroker


class Configurator:
    def __init__(self, broker: ServiceBroker):
        self._messageQueue = mp.Queue()
        self._sb = broker
        # register with sb as handler
        raise Exception('not implemented yet')

    def get_queue(self) -> mp.Queue:
        return self._messageQueue

    def start(self):
        raise Exception('not implemented yet')
