import multiprocessing as mp

class Configurator:
    def __init__(self):
        self._messageQueue = mp.Queue()
        raise Exception('not implemented yet')

    def getQueue(self) -> mp.Queue:
        return self._messageQueue

    def start(self):
        raise Exception('not implemented yet')