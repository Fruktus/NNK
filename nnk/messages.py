class CommandMessage:
    def __init__(self, target, source, args):
        self.target = target  # service or handler (checked in that order)
        self.source = source
        self.args = args
        # kwargs?

    def __str__(self):
        return '<CommandMessage> source:' + str(self.source) + ' target:' + str(self.target) + ' args:' + str(self.args)


class ConfigMessage:
    def __init__(self, target, source, config: dict = None):
        self.target = target  # the id of the service, same as in config
        # technically, it only needs one since there is only one configurator and broker can check the type

        self.source = source
        self.config = config

    def __str__(self):
        return '<ConfigMessage> source:' + str(self.source) + ' target:' + str(self.target) + ' config:' + str(self.config)
