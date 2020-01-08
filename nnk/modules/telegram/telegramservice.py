import logging
import multiprocessing as mp
from telegram import Bot

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
            # TODO register handler with broker
            message = self._ownqueue.get()
            if isinstance(message, ConfigMessage):
                self._load_config(message.config)
            if isinstance(message, CommandMessage):
                if message.target == Services.USER_TEXT_OUTPUT:
                    self._send_message(message.args)  # TODO possibly refactor
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
            return
        elif config['token'] == '':
            lg.warning('missing token, exiting')
            self.stop()
            return
        if config['chat_id'] == '@channelusername':
            lg.warning('missing chat id, exiting')
            self.stop()
            return

        # start telegram with token
        self._chat_id = config['chat_id']
        self._module = TelegramModule(config['token'])
        self._start_module()

    def _start_module(self):
        # FIXME tmp only, handlers should be declared elsewhere
        from telegram.ext import MessageHandler, Filters

        def echo(update, context):
            lg.debug(update.message.chat_id)  # tmp, for removal
            context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

        # used for forwarding user input to broker
        # TODO defined here temporarily, move someplace more fitting
        def message_handler(update, context):
            self._send_message_from_telegram(update.message.text.split())

        echo_handler = MessageHandler(Filters.text, echo)
        self._module.add_handler(echo_handler)
        self._module.add_handler(message_handler())
        self._module.start_telegram()
        # updater.idle() start polling is nonblocking so this might come in handy

    def _store_config(self):
        # send info to broker to pass through handler to configurator to add config
        msg = ConfigMessage(target=Services.CONFIG, source=self._id, config={'token': '', 'chat_id': '@channelusername'})
        self._brokerqueue.put(msg)

    # snippet, for later use in processing messages
    def _send_message(self, message: str):
        self._module.send_message(self._chat_id, message)

    # draft, will be called from handlers
    def _send_message_from_telegram(self, args):
        msg = CommandMessage(target=Services.USER_TEXT_INPUT, source=self._id, args=args)
        self._brokerqueue.put(msg)
