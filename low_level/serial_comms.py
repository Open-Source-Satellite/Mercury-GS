###################################################################################
# @file serial_comms.py
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
#  Mercury GS Low Level Driver
#  @author: Jamie Bayley (jbayley@kispe.co.uk)
###################################################################################
import queue
import struct
import threading
import time
import serial
from low_level.frameformat import PROTOCOL_DELIMITER, MAX_DATA_TYPES

frame_queue = queue.Queue()
direct_read_queue = queue.Queue()
serial_handler = None
PENDING_FRAME = 0
GATHERING_DATA = 1
READING_DATA = 2
DIRECT_READ = 3


class SerialHandler:
    def __init__(self, port, baud_rate):
        self.rx_listener = StateMachine()
        self.serial = SerialComms(port, baud_rate)


class SerialComms(serial.Serial):
    def __init__(self, port, baud_rate):
        super().__init__(port, baud_rate)
        self.bytesize = 8
        self.write_timeout = 5

        if self.is_open:
            self.close()

        if not self.is_open:
            self.open()

    def change_baud_rate(self, requested_baud_rate):
        if self.baudrate is not requested_baud_rate:
            return requested_baud_rate

    def send(self, data_to_send):
        try:
            self.write(bytearray(str(data_to_send), "utf8"))
        except serial.serialutil.SerialTimeoutException as err:
            print(repr(err))
            print("ERROR: Write Has Timed Out")


class StateMachine(threading.Thread):
    def __init__(self):
        super().__init__()
        self.packet_buffer = bytearray()
        self.delimiter_discarded = False
        self.test_listen = False
        self.test_listen_finish = False

    def run(self):
        while True:
            if self.test_listen is True:
                self.direct_read(serial_handler.serial)
            else:
                self.packet_buffer.clear()
                self.pending_frame(serial_handler.serial)

    def pending_frame(self, com):
        # Check if there is incoming data
        if com.in_waiting != 0:
            try:
                # Clear the received data buffer if it's 2 bytes
                if len(self.packet_buffer) == 2:
                    self.packet_buffer.clear()
            except TypeError as err:
                print("ERROR: ", err)
                print("FIRST PASS")

            # Read a byte
            rx_byte = self.read_byte(com)
            self.packet_buffer += rx_byte
            # Check if we have received a 0x55 followed by a non-0x55
            if (PROTOCOL_DELIMITER == self.packet_buffer[0]) and (rx_byte[0] != PROTOCOL_DELIMITER):
                # This is the start of a new frame!
                # Switch state to GATHERING_DATA and pass the 2 bytes of header data
                self.gathering_header(com)
            # Save the previous byte received if start of frame not detected
            self.pending_frame(com)

    def gathering_header(self, com):
        # Initialise Header Buffer
        header_size = 3
        gathered_header = bytearray()
        header_count = 0

        # Iterate over Header bytes
        while header_count < header_size:
            # Read a byte into Header Buffer
            gathered_header += self.read_byte(com)
            # Scan byte and previous byte for start of frame, pop off any double delimiter values
            gathered_header, header_count = self.x55_scan(gathered_header, header_count, com)
        self.delimiter_discarded = False

        # Append gathered header onto first 2 bytes passed into this state
        self.packet_buffer.extend(gathered_header)
        # Check if Data Type is within range
        if self.packet_buffer[4] in range(MAX_DATA_TYPES):
            # Data Type within range, switch to READING_DATA state and pass header data
            self.reading_data(com)
        else:
            # Data Type out of range, discard message and return to PENDING_FRAME
            self.pending_frame(com)

    def reading_data(self, com):
        # Create data length bitfield buffer
        data_length_size = 4
        data_length_bytes = bytearray()
        data_length_count = 0
        data_count = 0

        # Iterate over Data Length Bytes
        while data_length_count < data_length_size:
            # Read a byte into Data Length Buffer
            data_length_bytes += self.read_byte(com)
            # Scan byte and previous byte for start of frame, pop off any double delimiter values
            data_length_bytes, data_length_count = self.x55_scan(data_length_bytes, data_length_count, com)
        data_length = struct.unpack("!L", data_length_bytes)[0]

        self.delimiter_discarded = False
        data_bytes = bytearray()

        # Iterate over Data Bytes
        while data_count < data_length:
            # Read a byte into Data Buffer
            data_bytes += self.read_byte(com)
            # Scan byte and previous byte for start of frame, pop off any double delimiter values
            data_bytes, data_count = self.x55_scan(data_bytes, data_count, com)

        self.packet_buffer.extend(data_length_bytes + data_bytes)
        self.delimiter_discarded = False

        frame_queue.put(self.packet_buffer)
        time.sleep(1)

    def direct_read(self, com):
        if com.in_waiting != 0:
            # Read a byte
            rx_byte = self.read_byte(com)
            direct_read_queue.put(rx_byte)

    def read_byte(self, com):
        rx_byte = com.read(1)
        return rx_byte

    def x55_scan(self, buffer, index, com):
        # Check if this is the first byte
        if index > 0:
            # If byte is Header Value 0x55 and previous bytes is also 0x55
            if PROTOCOL_DELIMITER is buffer[index] and PROTOCOL_DELIMITER is self.packet_buffer[index - 1]:
                # A delimiter byte has been received, and the last byte was also a delimiter.
                # So Discard the byte
                buffer.pop(index)
                # Rewind indexer to maintain stepping
                index -= 1
                delimiter_discarded = True
            # If previous byte is a delimiter and we haven't discarded a byte
            elif PROTOCOL_DELIMITER is buffer[index - 1] and self.delimiter_discarded is False:
                # Start of Frame detected, discard message and start again
                self.gathering_header(com)
            else:
                self.delimiter_discarded = False
        # Increment the index
        index += 1

        return buffer, index


def serial_comms_init(port, baud_rate):
    global serial_handler
    serial_handler = SerialHandler(port, baud_rate)
    serial_handler.rx_listener.start()
