import logging
import multiprocessing as mp
from abc import ABC, abstractmethod

from nnk.messages import AbstractMessage


class AbstractModule(ABC):
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

    def send(self, msg: AbstractMessage):
        # TODO possibly rename
        self._brokerqueue.put(msg)
