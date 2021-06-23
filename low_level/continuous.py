from config import TIMEOUT
import low_level.serial_comms
from threading import Timer
import time

rt = None


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.next_call = time.time()
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self.next_call += self.interval
            self._timer = Timer(self.next_call - time.time(), self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


def register_continuous(calls_per_second, callback, data_to_send, message_object_database, latest_message_object):
    frequency = 1.0 / calls_per_second
    global rt
    rt = RepeatedTimer(frequency, callback, data_to_send, message_object_database, latest_message_object)


def adjust_continuous(calls_per_second):
    global rt
    if isinstance(rt, RepeatedTimer):
        frequency = 1.0 / calls_per_second
        rt.interval = frequency
        rt.stop()
        rt.start()


def continuous_stop():
    rt.stop()


def continuous_sender(frame, message_object_database, latest_message_object):
    new_object = latest_message_object.__class__(latest_message_object.ID, TIMEOUT)
    message_object_database.append(new_object)
    new_object.start_timer()
    low_level.serial_comms.serial_handler.serial.send(frame)
