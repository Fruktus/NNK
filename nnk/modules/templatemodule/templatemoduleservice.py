import multiprocessing as mp
from .templatemodule import TemplateModule


# TODO refactor idea: create abstract class for all other modules
class TemplatemoduleService:
    # follow this everywhere! (service parameters - two queues)
    def __init__(self, brokerqueue: mp.Queue, ownqueue: mp.Queue):
        self._brokerqueue = brokerqueue
        self._ownqueue = ownqueue
        self._id = 'templatemodule'
        self.tm = TemplateModule

    # follow this everywhere! (public method - start)
    def start(self):
        # if needed spawn child threads
        while True:
            message = self._ownqueue.get()
            # do some processing using the object

    def stop(self):
        # so that the module can save its config and exit gracefully
        raise NotImplementedError


