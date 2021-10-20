###################################################################################
# @file comms.py
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
#  Mercury GS Serial Driver
#  @author: Jamie Bayley (jbayley@kispe.co.uk)
###################################################################################
import queue
import struct
import threading
import time
import serial
import config
from low_level.frameformat import PROTOCOL_DELIMITER, MAX_DATA_TYPES, DataType, DataTypeSize

frame_queue = queue.Queue()
direct_read_queue = queue.Queue()
comms_handler = None
PENDING_FRAME = 0
GATHERING_DATA = 1
READING_DATA = 2
DIRECT_READ = 3


def comms_register_callback(exception_handler_function_ptr):
    """ Registers the callbacks for this module to pass data back to previous modules. """
    global callback_exception_handler
    # Set exception handler callback
    callback_exception_handler = exception_handler_function_ptr


class CommsHandler:
    """ A Class to handle the comms and rx_state_machine. """

    def __init__(self, port, baud_rate):
        """ Initialise the rx_listener and serial. """
        self.rx_state_machine = StateMachine()
        self.comms = SerialComms(port, baud_rate)


class SerialComms(serial.Serial):
    """ A Class to handle the serial comms through a UART. """

    def __init__(self, port, baud_rate):
        """ Initialise serial interface, set bytesize and write_timeout values. """
        try:
            super().__init__(port, baud_rate)
        except serial.serialutil.SerialException as err:
            print(repr(err))

        self.bytesize = 8
        self.write_timeout = 5

        # Close COM Port if open
        if self.is_open:
            self.close()

        # Open COM Port
        try:
            self.open()
        except serial.serialutil.SerialException as err:
            print(repr(err))

    def check_baud_rate(self, requested_baud_rate):
        """ Check that the baud rate requested is not already set. """
        if self.baudrate is not requested_baud_rate:
            return requested_baud_rate

    def send(self, data_to_send):
        """ Send data over the COM Port. """
        try:
            self.write(data_to_send)
        except serial.serialutil.SerialTimeoutException as err:
            print(repr(err))
            print("ERROR: Write Has Timed Out")
            callback_exception_handler("ERROR: Write Has Timed Out")
        except serial.serialutil.PortNotOpenError as err:
            print(repr(err))
            print("ERROR: Port" + config.COM_PORT + " Not Open")
            callback_exception_handler("ERROR: Port" + config.COM_PORT + " Not Open")
        except serial.serialutil.SerialException as err:
            print(repr(err))
            print("ERROR: The handle is invalid")
            callback_exception_handler("ERROR: The handle is invalid")


class StateMachine(threading.Thread):
    """ StateMachine Class for the RX_Listener running on a separate Thread. """

    def __init__(self):
        """ Initialise Thread, buffer and checking variables. """
        super().__init__()
        self.frame_buffer = bytearray()
        self.delimiter_received = False
        self.test_listen = False
        self.daemon = True

    def run(self):
        """ Overloads the Thread's "run" function,
        reads directly if Test Interface is used,
        otherwise engages StateMachine.
        """
        while True:
            if comms_handler.comms.is_open:
                if self.test_listen is True:
                    self.direct_read(comms_handler.comms)
                else:
                    self.frame_buffer.clear()
                    self.pending_frame(comms_handler.comms)

    def pending_frame(self, com):
        """ PENDING_FRAME State, checks for start of frame...
        (delimiter character followed by non delimiter character).
        """
        # Block until there is a byte to read
        rx_byte = self.read_byte(com)
        try:
            # Clear the received data buffer if it's 2 bytes
            if len(self.frame_buffer) == 2:
                self.frame_buffer.clear()
        except TypeError as err:
            print("ERROR: ", err)
            print("FIRST PASS")

        # Add byte to the frame buffer
        self.frame_buffer += rx_byte
        # Check if we have received a 0x55 followed by a non-0x55
        if (PROTOCOL_DELIMITER == self.frame_buffer[0]) and (rx_byte[0] != PROTOCOL_DELIMITER):
            # This is the start of a new frame!
            # Switch state to GATHERING_DATA
            self.gathering_header(com)
        # Reenter PENDING_FRAME if start of frame not detected
        self.pending_frame(com)

    def gathering_header(self, com):
        """ GATHERING_HEADER State, reads the rest of the header. """
        # Create header bitfield buffer
        header_size = 3
        gathered_header = bytearray()
        header_count = 0

        # Iterate over Header bytes
        while header_count < header_size:
            # Read a byte into Header Buffer
            gathered_header += self.read_byte(com)
            # Scan byte and previous byte for start of frame, pop off any double delimiter values
            gathered_header, header_count = self.delimiter_scan_and_remove(gathered_header, header_count, com)

        # Append gathered header onto buffer
        self.frame_buffer.extend(gathered_header)
        # Check if Data Type is within range
        if int(self.frame_buffer[4]) in range(MAX_DATA_TYPES):
            # Data Type within range, switch to READING_DATA state
            self.reading_data(com)
        else:
            # Data Type out of range, discard message and return to PENDING_FRAME
            self.pending_frame(com)

    def reading_data(self, com):
        """ READING_DATA State, gathers the data length field and reads the rest of the frame,
        then if frame is valid place onto queue to be processed by the packet handler Thread.
        """
        # Create data length bitfield buffer
        data_length_bytes = bytearray()
        data_length_size = 4
        data_length_count = 0
        data_count = 0

        # Iterate over Data Length bytes
        while data_length_count < data_length_size:
            # Read a byte into Data Length Buffer
            data_length_bytes += self.read_byte(com)
            # Scan byte and previous byte for start of frame, pop off any double delimiter values
            data_length_bytes, data_length_count = self.delimiter_scan_and_remove(data_length_bytes, data_length_count,
                                                                                  com)
        # unpacks data_length_bytes into 32 bit unsigned integer
        try:
            data_length = struct.unpack("!L", data_length_bytes)[0]
        except struct.error as err:
            print(repr(err))
            print("ERROR: Data Length is not 4 bytes")
            callback_exception_handler("ERROR: Data Length is not 4 bytes")

        # Create data bitfield buffer
        data_bytes = bytearray()

        # Iterate over Data Bytes
        while data_count < data_length:
            # Read a byte into Data Buffer
            data_bytes += self.read_byte(com)
            # Scan byte and previous byte for start of frame, pop off any double delimiter values
            data_bytes, data_count, data_length = self.delimiter_scan_and_remove(data_bytes, data_count, com, True,
                                                                                 data_length)

        self.delimiter_received = False
        invalid_frame = False
        data_type = self.frame_buffer[4]
        # Check the data type against all known data types
        if not any(x.value == data_type for x in DataType):
            invalid_frame = True
            callback_exception_handler("ERROR: Frame Data Type Field does not match actual type.")

        # Get the data type name to use with comparing against the right data length
        data_type_key = DataType(data_type).name

        # Check the actual data length against the expected length for the data type
        if data_length != DataTypeSize[data_type_key].value:
            invalid_frame = True
            callback_exception_handler("ERROR: Frame Data Length Field does not match actual length.")

        if invalid_frame is False:
            # Append data length and data fields onto frame buffer
            self.frame_buffer.extend(data_length_bytes + data_bytes)
            # Add Frame onto queue to be processed by packet handler Thread
            frame_queue.put(self.frame_buffer)
            # Block until packet is processed in handler Thread
            frame_queue.join()
        else:
            # Invalid frame, re-enter pending_frame() state
            self.pending_frame(com)

        # Clear the frame buffer
        self.frame_buffer.clear()

    def direct_read(self, com):
        """ DIRECT_READ State, entered if Test Interface is used to bypass State Machine """
        # Block until there is a byte to read
        rx_byte = self.read_byte(com)
        # Put byte onto queue
        direct_read_queue.put(rx_byte)

    @staticmethod
    def read_byte(com):
        """ Read and return a byte from the COM Port """
        rx_byte = com.read(1)
        return rx_byte

    def delimiter_scan_and_remove(self, buffer, index, com, data_field=False, data_length_decrement=0):
        """ Iterate through buffer, pop off a delimiter where there are 2 consecutive delimiter values,
        enter GATHERING_HEADER State if start of frame detected.
        """
        # If this byte is a delimiter
        if PROTOCOL_DELIMITER is buffer[index]:
            # and we haven't received a prior delimiter
            if self.delimiter_received is False:
                # Record that this byte is a delimiter
                self.delimiter_received = True
            # and we've received a prior valid delimiter
            else:
                # Discard the byte
                buffer.pop(index)
                # Rewind indexer to maintain stepping
                index -= 1
                if data_field is True:
                    # Add to data_length decrementer HERE to then take off data_length after entire read
                    data_length_decrement -= 1
                # Set state to wait for next delimiter
                self.delimiter_received = False
        # If this byte is not a delimiter
        else:
            # and we have received a prior delimiter that makes this an invalid sequence
            if self.delimiter_received is True:
                # This is the start of a new frame!
                # Set the frame buffer to this new frame
                self.frame_buffer = buffer
                # Reset received delimiter variable
                self.delimiter_received = False
                # Enter GATHERING_HEADER state
                self.gathering_header(com)
        # Increment the index
        index += 1
        if data_length_decrement == 0:
            return buffer, index
        else:
            return buffer, index, data_length_decrement


def comms_init(port, baud_rate):
    """ Initialise CommsHandler class instance , set COM Port and baud rate, start rx_listener Thread. """
    global comms_handler
    if comms_handler is not CommsHandler:
        comms_handler = CommsHandler(port, baud_rate)
        comms_handler.rx_state_machine.start()


def comms_send(data):
    """ Send data over the COM Port"""
    comms_handler.comms.send(data)


def change_baud_rate(requested_baud_rate):
    """ Change baud rate to requested rate """
    global comms_handler
    comms_handler.comms.baudrate = comms_handler.comms.check_baud_rate(requested_baud_rate)


def flush_com_port():
    global comms_handler
    comms_handler.comms.reset_output_buffer()


def change_com_port(port):
    global comms_handler
    comms_handler.comms.close()
    comms_handler.comms.port = port
    config.COM_PORT = port
    try:
        comms_handler.comms.open()
    except serial.serialutil.SerialException as err:
        print(repr(err))
