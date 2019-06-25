from .templatemodule import TemplateModule


class TemplateModuleService:
    # follow this everywhere! (service parameters - two queues)
    def __init__(self, brokerqueue, ownqueue):
        self.brokerqueue = brokerqueue
        self.ownqueue = ownqueue
        self.tm = TemplateModule

    # follow this everywhere! (public method - start)
    def start(self):
        # if needed spawn child threads
        while True:
            self.ownqueue.get()
            # do some processing using the object
