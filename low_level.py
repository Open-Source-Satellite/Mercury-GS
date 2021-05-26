###################################################################################
# @file low_level.py
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
import threading
import time

import serial

frame_queue = queue.Queue()

import config
from serial_framing.frameformat import PROTOCOL_DELIMITER, MAX_DATA_TYPES
import struct

frame_queue = queue.Queue()

ser = serial.Serial()
PENDING_FRAME = 0
GATHERING_DATA = 1
READING_DATA = 2
packet_buffer = None


def register_callback(packet_handler_thread_start_ptr):
    global callback_packet_handler_thread_start
    callback_packet_handler_thread_start = packet_handler_thread_start_ptr


def rx_listener(com):
    while True:
        frame = [bytes([0])]
        switch_states(PENDING_FRAME, com, frame)


def read_byte(com):
    rx_byte = com.read(1)
    return rx_byte


rx_listener_thread = threading.Thread(target=rx_listener, args=(ser,))


def send(data_to_send):
    change_baud_rate(config.BAUD_RATE)
    print(ser.name)
    print(ser.baudrate)
    ser.write(bytearray(str(data_to_send), "utf8"))


def init():
    change_baud_rate(config.BAUD_RATE)
    ser.port = 'COM19'
    ser.bytesize = 8
    # ser.write_timeout = 5

    if ser.is_open:
        ser.close()

    if not ser.is_open:
        ser.open()

    print(ser.is_open)
    if not rx_listener_thread.is_alive():
        rx_listener_thread.start()


def change_baud_rate(requested_baud_rate):
    if ser.baudrate is not requested_baud_rate:
        ser.baudrate = requested_baud_rate


def pending_frame(com, header_data):
    # Check if there is incoming data
    if com.in_waiting != 0:
        # Read a byte
        rx_byte = read_byte(com)
        try:
            delimiter_test = int.from_bytes(header_data[0], "little")
            # Check if we have received a 0x55 followed by a non-0x55
            if (PROTOCOL_DELIMITER == delimiter_test) and (rx_byte != PROTOCOL_DELIMITER):
                # This is the start of a new frame!
                # Collect first two bytes of header
                header_data = [bytes([PROTOCOL_DELIMITER]), rx_byte]
                # Switch state to GATHERING_DATA and pass the 2 bytes of header data
                switch_states(GATHERING_DATA, com, header_data)
            # Save the previous byte received if start of frame not detected
        finally:
            header_data[0] = rx_byte
            switch_states(PENDING_FRAME, com, header_data)


def gathering_header(com, header_data):
    # Initialise Header Buffer
    header_size = 3
    gathered_header = [0, 0, 0]
    delimiter_byte_received = False
    count = 0

    # Iterate over Header bytes
    while count < header_size:
        # Read a byte into Header Buffer
        gathered_header[count] = read_byte(com)
        # Scan byte and previous byte for start of frame, pop off any double delimiter values
        gathered_header, count, delimiter_byte_received = x55_scan(gathered_header, count, delimiter_byte_received, com)

    # Append gathered header onto first 2 bytes passed into this state
    header_data.extend(gathered_header)
    # Check if Data Type is within range
    if int.from_bytes(header_data[4], "little") in range(MAX_DATA_TYPES):
        # Data Type within range, switch to READING_DATA state and pass header data
        switch_states(READING_DATA, com, header_data)
    else:
        # Data Type out of range, discard message and return to PENDING_FRAME
        switch_states(PENDING_FRAME, com)


def reading_data(com, data):
    # Create data length bitfield buffer
    data_length_bytes = [0, 0, 0, 0]
    delimiter_byte_received = False
    data_length_size = 4
    data_length_count = 0
    data_count = 0

    # Iterate over Data Length Bytes
    while data_length_count < data_length_size:
        # Read a byte into Data Length Buffer
        data_length_bytes[data_length_count] = read_byte(com)
        # Scan byte and previous byte for start of frame, pop off any double delimiter values
        data_length_bytes, data_length_count, delimiter_byte_received = x55_scan(data_length_bytes, data_length_count,
                                                                                 delimiter_byte_received, com)

    data_length = struct.unpack("!L", b"".join(data_length_bytes))[0]

    delimiter_byte_received = False
    data_bytes = [0] * data_length

    # Iterate over Data Bytes
    while data_count < data_length:
        # Read a byte into Data Buffer
        data_bytes[data_count] = read_byte(com)
        # Scan byte and previous byte for start of frame, pop off any double delimiter values
        data_bytes, data_count, delimiter_byte_received = x55_scan(data_bytes, data_count, delimiter_byte_received, com)

    data.extend(data_length_bytes + data_bytes)

    frame_queue.put(data)
    time.sleep(1)
    callback_packet_handler_thread_start()

    switch_states(PENDING_FRAME, com)


state_switch = {
    0: pending_frame,
    1: gathering_header,
    2: reading_data
}


def switch_states(switch, com, data=None):
    state_switch[switch](com, data)


def x55_scan(buffer, index, delimiter_received, com):
    # If byte is Header Value 0x55
    if PROTOCOL_DELIMITER in buffer[index]:
        # Check if this is the first byte
        if buffer[index] > 0:
            if (PROTOCOL_DELIMITER in buffer[index - 1]) and delimiter_received is False:
                # A delimiter byte has been received, but the last byte was not a delimiter.
                delimiter_byte_received = True
            elif (PROTOCOL_DELIMITER in buffer[index - 1]) and delimiter_received is True:
                # A delimiter byte has been received, and the last byte was also a delimiter.
                # So Discard the byte
                buffer.pop(index)
                # Rewind indexer to maintain stepping
                index -= 1
            elif PROTOCOL_DELIMITER in buffer[index - 1]:
                # Start of Frame detected
                switch_states(GATHERING_DATA, com, [PROTOCOL_DELIMITER, buffer[index]])
    index += 1

    return buffer, index, delimiter_received
