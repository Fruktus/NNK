import threading
from abc import ABC, abstractmethod
import multiprocessing as mp
import logging


def threaded(name=None, daemon=False):
    def threaded_wrapper(fn):
        def wrapper(*args, **kwargs):
            threading.Thread(target=fn, args=args, kwargs=kwargs, name=name, daemon=daemon).start()
        return wrapper
    return threaded_wrapper


# TODO figure out where template should be stored
class TMS(ABC):
    def __init__(self, brokerqueue: mp.Queue, ownqueue: mp.Queue, module_id: str):
        self._brokerqueue = brokerqueue
        self._ownqueue = ownqueue
        self._id = module_id
        self._lg = logging.getLogger('modules.' + self._id)  # like this or module-global?

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def send(self, msg):
        # will be implemented, for sending messages to broker, possibly rename for clarity
        pass
