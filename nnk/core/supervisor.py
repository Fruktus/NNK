import logging

from nnk.core.servicebroker import ServiceBroker
from nnk.core.loader import Loader
from nnk.core.configurator import Configurator
from nnk.utilities import threaded

lg = logging.getLogger('core.supervisor')


class Supervisor:
    def __init__(self, enable_status = False):
        self.sb = ServiceBroker()
        self.cf = Configurator(self.sb)
        self.ld = Loader(self.sb)

        self._enable_status = enable_status

    def start(self):
        lg.info('starting')
        self.sb.start()
        self.cf.start()
        self.ld.start()

        if self._enable_status:
            self._system_status_service()


    def stop(self):
        self.ld.stop()
        self.cf.stop()
        self.sb.stop()
        # stop own thread for status read?

    # TODO: just a draft, rename, test etc
    # parametrize whether should start
    @threaded(name='status_service', daemon=True)  # tmp only, should be joined and the queue needs to be deleted
    def _system_status_service(self):
        # will wait for clients to open pipe and write commands (newline terminated)
        # to check for status, will then respond with status
        # when client disconnects will reopen pipe
        import os
        try:
            fifo = 'myfifo'  # parametrize
            os.mkfifo(fifo)
            while True:
                with open(fifo) as fifo:
                    for line in fifo:
                        print(line)
        except OSError:
            # named pipes can only run on unix, but they are not critical for normal functioning
            lg.warning('named pipes are not supported by current OS')
