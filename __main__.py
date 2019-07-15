import logging
import time

from nnk.core.servicebroker import ServiceBroker
from nnk.core.loader import Loader
from nnk.core.configurator import Configurator


# overseer function, would build all required objects, start all of them and block/wait/whtvr
# possibly add handlers for signals or smth for supervisors
def main():
    logging.basicConfig(level=logging.DEBUG, format='{asctime} {name:<20} {levelname:10s} {message}', style='{')
    # https://pypi.org/project/multiprocessing-logging/
    # above might be useful but it didnt work on windows, maybe on linux it will (mp's limitations

    sb = ServiceBroker()
    cf = Configurator(sb)
    ld = Loader(sb)
    sb.start()
    cf.start()
    ld.start()

    # possibly rewrite without decorator and with events to stop threads properly (so i wont get broken pipe error)

    try:
        while True:
            # print(threading.enumerate())  # method to show all running threads
            time.sleep(36000)
    except KeyboardInterrupt:
        logging.info('exiting')
        cf.stop()
        ld.stop()
        sb.stop()

if __name__ == '__main__':
    main()
