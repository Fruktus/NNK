from abc import ABC

from nnk.constants import Services


class AbstractMessage(ABC):
    pass


class CommandMessage(AbstractMessage):
    def __init__(self, target: str, source: str, args: []):
        self.target = target  # service or handler (checked in that order)
        self.source = source
        self.args = args
        # kwargs?

    def __str__(self):
        return '<CommandMessage> source:' + str(self.source) + ' target:' + str(self.target) + ' args:' + str(self.args)


class ConfigMessage(AbstractMessage):
    def __init__(self, target: str, source: str, config: dict = None):
        self.target = target  # the id of the service, same as in config
        # technically, it only needs one since there is only one configurator and broker can check the type

        self.source = source
        self.config = config

    def __str__(self):
        return '<ConfigMessage> source:' + str(self.source) + ' target:' + str(self.target) + ' config:' + str(self.config)


class RegistrationMessage(AbstractMessage):
    """used by processes to register commands, processors and handlers. Target is always ServiceBroker.
    Requires the service to be added beforehand by the loader (because of the multiprocessing's queues limitation)"""
    def __init__(self, source: str, aliases: [str] = None, commands: [str] = None, handlers: [Services] = None,
                 processors: [] = None):
        self.source = source  # the id of service which provides given functionalities
        self.aliases = aliases  # the array of strings under which the module should be recognized
        self.commands = commands  # a string array of keywords recognized as commands
        self.handlers = handlers  # a list of handlers [Service constants] that the service supports
        self.processors = processors  # TODO same as above, right now placeholder only

    def __str__(self):
        return '<RegistrationMessage> source: ' + str(self.source) + ' aliases: ' + str(self.aliases) +\
               ' commands: ' + str(self.commands) + ' handlers: ' + str(self.handlers) + ' processors: ' +\
               str(self.processors)
