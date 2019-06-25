from nnk.core.servicebroker import ServiceBroker
from nnk.core.loader import Loader
from nnk.core.configurator import Configurator


# overseer function, would build all required objects, start all of them and block/wait/whtvr
# possibly add handlers for signals or smth for supervisors
def main():
    sb = ServiceBroker()
    ld = Loader(sb)
    cf = Configurator(sb)
    sb.start()


if __name__ == '__main__':
    main()
