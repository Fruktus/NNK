import logging
import multiprocessing as mp
import configparser as cp
from os.path import isfile

from nnk.core.servicebroker import ServiceBroker
from nnk.messages import CommandMessage, ConfigMessage
from nnk.constants import Services
from nnk.utilities import threaded

lg = logging.getLogger('core.configurator')


class Configurator:
    def __init__(self, broker: ServiceBroker):
        self._messageQueue = mp.Queue()
        self._sb = broker
        self._sb.add_handler(Services.CONFIG, self._messageQueue)
        self._config = cp.ConfigParser()
        self._file_modified = False

    def get_queue(self) -> mp.Queue:
        return self._messageQueue

    @threaded(name='configurator', daemon=True)  # TODO for removal, need to store the reference to thread
    def start(self):
        lg.info('starting')
        self.load_file()
        while True:
            msg = self._messageQueue.get()
            if isinstance(msg, ConfigMessage):
                lg.debug('received config request: %s', msg.source)
                self._process_config_request(msg.source, msg.config)
            if isinstance(msg, CommandMessage):
                raise NotImplementedError('configurator')

    def stop(self):
        if self._file_modified:
            self.save_file()

        self._messageQueue.close()
        self._messageQueue.join_thread()

    def load_file(self, path='config.ini'):
        if isfile(path):
            lg.info('loading config file')
            with open(path, 'r') as configfile:
                self._config.read_file(configfile)

        else:
            lg.info('config file not found')

    def save_file(self, path='config.ini'):
        with open(path, 'w') as configfile:
            self._config.write(configfile)

    def add_section(self, name: str):
        # should add the section name (after checking for doubles)
        # perhaps also the data or do that somewhere else
        # TODO would be good idea to allow adding whole dict at once
        if self._config.has_section(name):
            return
        self._config.add_section(name)

    def get_section(self, section: str):
        # should get the whole section, pack it and return
        # if not found return None
        if not self._config.has_section(section):
            return None
        return self._config[section]

    def del_section(self, section: str):
        if not self._config.has_section(section):
            return
        self._config.remove_section(section)

    def set_key(self, section: str, option: str, value: any):
        if not self._config.has_section(section):
            return
        self._config.set(section, option, value)

    def get_key(self, section: str, option: str):
        if not self._config.has_section(section):
            return None
        if not self._config.has_option(section, option):
            return None
        return self._config.get(section, option)

    def del_key(self, section: str, option: str):
        if not self._config.has_section(section):
            return None
        if not self._config.has_option(section, option):
            return None
        self._config.remove_option(section, option)

    def _process_config_request(self, source: str, config: dict):
        if not config:
            if self._config.has_section(source):
                msg = ConfigMessage(target=source, config=self.get_section(source), source='config')
                self._sb.get_queue().put(msg)
                lg.debug('providing requested config: %s', source)
            else:
                msg = ConfigMessage(target=source, config=None, source='config')
                self._sb.get_queue().put(msg)
                lg.debug('requested config not found: %s', source)
        else:
            lg.debug('modifying config: %s', source)
            if not self._config.has_section(source):
                self.add_section(source)
            for k, v in config.items():
                self.set_key(source, k, v)