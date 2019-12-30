import logging
import time

from nnk.core.supervisor import Supervisor


# overseer function, would build all required objects, start all of them and block/wait/whtvr
# possibly add handlers for signals or smth for supervisors
def main():
    logging.basicConfig(level=logging.DEBUG, format='{asctime} {name:<20} {levelname:10s} {message}', style='{')
    # https://pypi.org/project/multiprocessing-logging/
    # above might be useful but it didnt work on windows, maybe on linux it will (mp's limitations)
    # followup: after dockerizing worked nicely

    sv = Supervisor()
    sv.start()

    # possibly rewrite without decorator and with events to stop threads properly (so i wont get broken pipe error)

    try:
        while True:
            # print(threading.enumerate())  # method to show all running threads
            time.sleep(36000)
    except KeyboardInterrupt:
        logging.info('exiting')
        sv.stop()


if __name__ == '__main__':
    main()
