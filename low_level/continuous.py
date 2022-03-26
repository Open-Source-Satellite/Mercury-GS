###################################################################################
# @file continuous.py
###################################################################################
#   _  _____ ____  ____  _____
#  | |/ /_ _/ ___||  _ \| ____|
#  | ' / | |\___ \| |_) |  _|
#  | . \ | |___ ) |  __/| |___
#  |_|\_\___|____/|_|   |_____|
###################################################################################
# Copyright (c) 2020 KISPE Space Systems Ltd.
#
# Please follow the following link for the license agreement for this code:
# www.kispe.co.uk/projectlicenses/RA2001001003
###################################################################################
#  Created on: 06-May-2021
#  Mercury GS Continuous Transmission Handling
#  @author: Jamie Bayley (jbayley@kispe.co.uk)
###################################################################################
import config
from low_level.comms import flush_com_port, comms_send
from threading import Timer
import time


def continuous_register_callback(exception_handler_function_ptr):
    """ Registers the callbacks for this module to pass data back to previous modules. """
    global callback_exception_handler
    # Register exception handler callback
    callback_exception_handler = exception_handler_function_ptr


class RepeatedTimer(object):
    """ RepeatedTimer class to enable continuous transmission. """
    def __init__(self, interval, function, *args, **kwargs):
        """ Initialise the timer, set interval, function callback and args, then start the Timer. """
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.next_call = time.time()
        self.start()

    def _run(self):
        """ Start next Timer interval and call the associated function. """
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        """ Set up next Timer interval. """
        if not self.is_running:
            self.next_call += self.interval
            self._timer = Timer(self.next_call - time.time(), self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        """ Stop the Timer"""
        self._timer.cancel()
        self.is_running = False


def dummy_function():
    """ A dummy function to enable creating the Timer global"""
    pass


rt = RepeatedTimer((1.0 / config.TC_TLM_RATE), dummy_function)


def register_continuous(calls_per_second, callback, data_to_send, message_object_database, latest_message_object):
    """ Register a new continuous transmission Thread.
    Set the interval, callback function, arguments and then start the Thread.
    """
    frequency = 1.0 / calls_per_second
    global rt
    rt.interval = frequency
    rt.function = callback
    rt.args = (data_to_send, message_object_database, latest_message_object)#
    rt.start()


def adjust_continuous(calls_per_second):
    """ Adjust the continuous transmission Thread with a new rate"""
    global rt
    try:
        frequency = 1.0 / calls_per_second
        rt.interval = frequency
    except ZeroDivisionError as err:
        print("\n", repr(err))
        print("ERROR: Rate is 0, cannot run continuously")
        # callback_exception_handler("ERROR: Rate is 0, cannot run continuously")


def continuous_stop():
    """ Stop the continuous transmission thread """
    if rt.is_running is True:
        rt.stop()
        flush_com_port()


def continuous_sender(frame, message_object_database, latest_message_object):
    """ The function for each continuous transmission Thread. """
    # Create a new object for the message, pass in the ID and TIMEOUT value
    new_object = latest_message_object.__class__(latest_message_object.ID, config.TIMEOUT)
    # Append message to database so that a response can search for and cancel the timeout
    message_object_database.append(new_object)
    # Start the time
    new_object.start_timer()
    # Send the message
    comms_send(frame)
