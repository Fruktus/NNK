import logging
import multiprocessing as mp

from nnk.messages import CommandMessage, ConfigMessage
from nnk.constants import Services
from .telegram import TelegramModule

lg = logging.getLogger('modules.telegram')


class TelegramService:
    def __init__(self, brokerqueue: mp.Queue, ownqueue: mp.Queue):
        self._brokerqueue = brokerqueue
        self._ownqueue = ownqueue
        self._id = 'telegram'

    def start(self):
        # if needed, spawn child threads
        cfg = ConfigMessage(target=Services.CONFIG, source=self._id)
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
        # TODO: stop telegram if running, stop all child threads if needed
        pass

    def _load_config(self, config: dict):
        # the config is the response from configurator, may be empty
        if not config:
            lg.warning('storing initial config and exiting')
            self._store_config()
            self.stop()
        elif config['token'] == '':
            lg.warning('missing token, exiting')
            self.stop()

        # do not store the token itself, not necessary
        # start telegram with token
        self._module = TelegramModule(config['token'])
        self._start_module()

    def _start_module(self):
        # FIXME tmp only, handlers should be declared elsewhere
        from telegram.ext import MessageHandler, Filters

        def echo(update, context):
            context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

        echo_handler = MessageHandler(Filters.text, echo)
        self._module.add_handler(echo_handler)
        self._module.start_telegram()

    def _store_config(self):
        # send info to broker to pass through handler to configurator to add config
        msg = ConfigMessage(target=Services.CONFIG, source=self._id, config={'token': ''})
        self._brokerqueue.put(msg)

    # draft, will be called from handlers
    # def _send_message_from_telegram(self, args):
    #     msg = CommandMessage(target=Services.USER_TEXT_INPUT, source=self._id, args=args)
    #     self._brokerqueue.put(msg)
