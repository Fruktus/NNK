import logging
import multiprocessing as mp

from nnk.messages import CommandMessage, ConfigMessage

lg = logging.getLogger('modules.telegram')


class TelegramService:
    # follow this everywhere! (service parameters - two queues)
    def __init__(self, brokerqueue: mp.Queue, ownqueue: mp.Queue):
        self._brokerqueue = brokerqueue
        self._ownqueue = ownqueue
        self._id = 'telegram'

    # follow this everywhere! (public method - start)
    def start(self):
        # if needed, spawn child threads
        cfg = ConfigMessage(target='config', source=self._id)
        self._brokerqueue.put(cfg)
        lg.debug('requesting config')

        while True:
            message = self._ownqueue.get()
            if isinstance(message, ConfigMessage):
                self._load_config(message.config)
            if isinstance(message, CommandMessage):
                pass
                # do some processing using the object

        # for testing purposes
        # import time
        # while True:
        #     msg = CommandMessage('broker', args=None, source='telegram')
        #     self._brokerqueue.put(msg)
        #     time.sleep(10)

    def stop(self):
        # so that the module can save its config and exit gracefully
        raise NotImplementedError

    def _load_config(self, config: dict):
        # the dict is the response from configurator, may be empty!
        if not config:
            lg.debug('storing initial config')
            msg = ConfigMessage(target='config', source=self._id, config={'token': ''})
            self._brokerqueue.put(msg)
            return

        # i can use this method to process reply with config <-- this one looks best
        # needs to retrieve the token from config
        # raise NotImplementedError

    def _store_config(self):
        # send info to broker to pass through handler to configurator to add config
        # can pass something like token=fillme
        raise NotImplementedError
