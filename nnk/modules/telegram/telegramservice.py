import logging
import multiprocessing as mp

from nnk.messages import CommandMessage, ConfigMessage
from .telegram import TelegramModule

lg = logging.getLogger('modules.telegram')


class TelegramService:
    def __init__(self, brokerqueue: mp.Queue, ownqueue: mp.Queue):
        self._brokerqueue = brokerqueue
        self._ownqueue = ownqueue
        self._id = 'telegram'

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
        # TODO: stop telegram
        # raise NotImplementedError
        pass

    def _load_config(self, config: dict):
        # the dict is the response from configurator, may be empty!
        if not config:
            lg.warning('storing initial config and exiting')
            msg = ConfigMessage(target='config', source=self._id, config={'token': ''})
            self._brokerqueue.put(msg)
            self.stop()
        # TODO: telegram requires token to work, should exit if not supplied
        # i can use this method to process reply with config <-- this one looks best
        # needs to retrieve the token from config
        # raise NotImplementedError
        self.token = config['token']
        # start telegram with token
        self.module = TelegramModule(self.token)
        self._start_module()

    def _start_module(self):
        # FIXME tmp only
        def echo(update, context):
            context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

        from telegram.ext import MessageHandler, Filters
        echo_handler = MessageHandler(Filters.text, echo)
        self.module.add_handler(echo_handler)
        self.module.start_telegram()

    def _store_config(self):
        # send info to broker to pass through handler to configurator to add config
        # can pass something like token=fillme
        raise NotImplementedError
