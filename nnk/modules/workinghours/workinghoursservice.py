import logging
import multiprocessing as mp
import datetime
import pickle
from os.path import exists

from nnk.messages import CommandMessage, ConfigMessage, RegistrationMessage
from nnk.constants import Services

lg = logging.getLogger('modules.workinghours')


class WorkinghoursService:
    def __init__(self, brokerqueue: mp.Queue, ownqueue: mp.Queue):
        self._brokerqueue = brokerqueue
        self._ownqueue = ownqueue
        self._id = 'workinghours'
        self._default_path = 'workinghours.dat'
        self._work_data = {}

    def start(self):
        if exists(self._default_path):
            with open(self._default_path, 'rb') as data_dict_file:
                self._work_data = pickle.load(data_dict_file)
        self._brokerqueue.put(RegistrationMessage(source=self._id,
                                                  commands=['get', '']))

        while True:
            message = self._ownqueue.get()
            if isinstance(message, CommandMessage):
                if message.args[1] == 'get':
                    self.get_hours()
                else:
                    self.add_hours(message.args[1])

    def stop(self):
        with open(self._default_path, 'wb') as data_dict_file:
            pickle.dump(self._work_data, data_dict_file)

    def add_hours(self, hours):
        # parse the hours, if they are as 8h then 8, if 8:00-17:00 then 9
        today = datetime.date.today()
        self._work_data[today] = hours
        total = 0
        for k, v in self._work_data.items():
            date = datetime.datetime.strptime(k, '%Y-%m-%d')
            if date.month == today.month:
                total += self._work_data[date]
        with open(self._default_path, 'wb') as data_dict_file:  # TMP remove when stopping is properly implemented
            pickle.dump(self._work_data, data_dict_file)        # TMP ...
        self._brokerqueue.put(CommandMessage(target=Services.USER_TEXT_OUTPUT,
                                             args="added {0} hours.\nThis month you worked for {1} \
                                             hours this month".format(hours, total),
                                             source=self._id))

    def get_hours(self):
        self._brokerqueue.put(CommandMessage(target=Services.USER_TEXT_OUTPUT,
                                             args=str(self._work_data),
                                             source=self._id))