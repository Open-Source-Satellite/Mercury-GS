###################################################################################
# @file test.py
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
#  Mercury GS Test Interface
#  @author: Jamie Bayley (jbayley@kispe.co.uk)
###################################################################################
import codecs
from threading import Timer
import low_level.comms


class TestFrame:
    def __init__(self, delimiter, reserved_bytes, data_type, data_length, data_field):
        self.delimiter = self.bytes_from_string(delimiter)
        self.reserved_bytes = self.bytes_from_string("".join(reserved_bytes))
        self.data_type = self.bytes_from_string(data_type)
        self.data_length = self.bytes_from_string(data_length)
        self.data_field = self.bytes_from_string(data_field)
        self.bytes_to_send = self.join_bytes()
        self.TimerFunction = Timer(5, self.read_finished)
        self.test_response = bytes()

    @staticmethod
    def bytes_from_string(hex_string):
        # Remove Whitespace
        hex_string = hex_string.replace(" ", "")
        # Replace 0x with \x as \x is string representation of hex, 0x is numerical
        hex_string = hex_string.replace("0x", r"\x")
        hex_string = codecs.decode(hex_string, "unicode_escape")
        # Convert hex string to binary
        bytes_to_return = bytes(hex_string, "utf8")
        return bytes_to_return

    def join_bytes(self):
        bytes_buffer = self.delimiter + self.reserved_bytes + self.data_type + self.data_length + self.data_field
        return bytes_buffer

    def transmit(self):
        low_level.comms.serial_handler.comms.send(self.bytes_to_send)
        low_level.comms.serial_handler.rx_state_machine.test_listen = True
        self.TimerFunction.start()

    def read_finished(self):
        low_level.comms.serial_handler.rx_state_machine.test_listen = False
        while low_level.comms.direct_read_queue.qsize() > 0:
            self.test_response += low_level.comms.direct_read_queue.get()

        test_response_string = self.test_response.hex("x", 1)
        test_response_string = test_response_string.replace("x", " 0x")
        test_response_string = "0x" + test_response_string
        callback_test_response(test_response_string)
        # self.test_response.clear()


def test_register_callback(test_response_function_ptr, exception_handler_function_ptr):
    """ Registers the callbacks for this module to pass data back to previous modules. """
    global callback_test_response
    global callback_exception_handler
    # Register callback to update GUI with Test Result
    callback_test_response = test_response_function_ptr
    # Set exception handler callback
    callback_exception_handler = exception_handler_function_ptr


def transmit_test_frame(delimiter, reserved_bytes, data_type, data_length, data_field):
    test_frame = TestFrame(delimiter, reserved_bytes, data_type, data_length, data_field)
    test_frame.transmit()
