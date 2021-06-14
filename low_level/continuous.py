from low_level.serial_comms import send
import threading
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
            self._timer = threading.Timer(self.next_call - time.time(), self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


def register_continuous(calls_per_second, callback, data_to_send):
    frequency = 1.0 / calls_per_second
    global rt
    rt = RepeatedTimer(frequency, callback, data_to_send)  # it auto-starts, no need of rt.start()


def adjust_continuous(calls_per_second):
    frequency = 1.0 / calls_per_second
    global rt
    rt.interval = frequency
    rt.stop()
    rt.start()


def continuous_stop():
    rt.stop()


def continuous_sender(frame):
    send(frame)
