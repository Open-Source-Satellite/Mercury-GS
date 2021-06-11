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
import config
from serial_framing.frameformat import PROTOCOL_DELIMITER, MAX_DATA_TYPES
import struct

frame_queue = queue.Queue()

# CONDITION = threading.Condition()

ser = serial.Serial()
PENDING_FRAME = 0
GATHERING_DATA = 1
READING_DATA = 2
packet_buffer = None


def rx_listener(com):
    # CONDITION.wait()
    while True:
        frame = bytearray()
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

    if not rx_listener_thread.is_alive():
        rx_listener_thread.start()


def change_baud_rate(requested_baud_rate):
    if ser.baudrate is not requested_baud_rate:
        ser.baudrate = requested_baud_rate


def pending_frame(com, header_data):
    # Check if there is incoming data
    if com.in_waiting != 0:

        try:
        # Clear the received data buffer if it's 2 bytes
            if len(header_data) == 2:
                header_data.clear()
        except TypeError as err:
            print("ERROR: ", err)
            print("FIRST PASS")

        # Read a byte
        rx_byte = read_byte(com)
        header_data += rx_byte
        # Check if we have received a 0x55 followed by a non-0x55
        if (PROTOCOL_DELIMITER == header_data[0]) and (rx_byte[0] != PROTOCOL_DELIMITER):
            # This is the start of a new frame!
            # Switch state to GATHERING_DATA and pass the 2 bytes of header data
            switch_states(GATHERING_DATA, com, header_data)
        # Save the previous byte received if start of frame not detected
        switch_states(PENDING_FRAME, com, header_data)


def gathering_header(com, header_data):
    # Initialise Header Buffer
    header_size = 3
    gathered_header = bytearray()
    delimiter_byte_discarded = False
    header_count = 0

    # Iterate over Header bytes
    while header_count < header_size:
        # Read a byte into Header Buffer
        gathered_header += read_byte(com)
        # Scan byte and previous byte for start of frame, pop off any double delimiter values
        gathered_header, header_count, delimiter_byte_discarded = x55_scan(gathered_header, header_count,
                                                                           delimiter_byte_discarded, com)

    # Append gathered header onto first 2 bytes passed into this state
    header_data.extend(gathered_header)
    # Check if Data Type is within range
    if header_data[4] in range(MAX_DATA_TYPES):
        # Data Type within range, switch to READING_DATA state and pass header data
        switch_states(READING_DATA, com, header_data)
    else:
        # Data Type out of range, discard message and return to PENDING_FRAME
        switch_states(PENDING_FRAME, com)


def reading_data(com, data):
    # Create data length bitfield buffer
    data_length_size = 4
    data_length_bytes = bytearray()
    data_length_count = 0
    data_count = 0
    delimiter_byte_discarded = False

    # Iterate over Data Length Bytes
    while data_length_count < data_length_size:
        # Read a byte into Data Length Buffer
        data_length_bytes += read_byte(com)
        # Scan byte and previous byte for start of frame, pop off any double delimiter values
        data_length_bytes, data_length_count, delimiter_byte_discarded = x55_scan(data_length_bytes, data_length_count,
                                                                                  delimiter_byte_discarded, com)

    data_length = struct.unpack("!L", data_length_bytes)[0]

    delimiter_byte_discarded = False
    data_bytes = bytearray()

    # Iterate over Data Bytes
    while data_count < data_length:
        # Read a byte into Data Buffer
        data_bytes += read_byte(com)
        # Scan byte and previous byte for start of frame, pop off any double delimiter values
        data_bytes, data_count, delimiter_byte_discarded = x55_scan(data_bytes, data_count, delimiter_byte_discarded,
                                                                    com)

    data.extend(data_length_bytes + data_bytes)

    frame_queue.put(data)
    time.sleep(1)
    # CONDITION.wait()
    rx_listener(com)


state_switch = {
    0: pending_frame,
    1: gathering_header,
    2: reading_data
}


def switch_states(switch, com, data=None):
    state_switch[switch](com, data)


def x55_scan(buffer, index, delimiter_discarded, com):
    # Check if this is the first byte
    if index > 0:
        # If byte is Header Value 0x55 and previous bytes is also 0x55
        if PROTOCOL_DELIMITER is buffer[index] and PROTOCOL_DELIMITER is buffer[index - 1]:
            # A delimiter byte has been received, and the last byte was also a delimiter.
            # So Discard the byte
            buffer.pop(index)
            # Rewind indexer to maintain stepping
            index -= 1
            delimiter_discarded = True
        # If previous byte is a delimiter and we haven't discarded a byte
        elif PROTOCOL_DELIMITER is buffer[index - 1] and delimiter_discarded is False:
            # Start of Frame detected, discard message and start again
            switch_states(GATHERING_DATA, com, buffer)
        else:
            delimiter_discarded = False
    # Increment the index
    index += 1

    return buffer, index, delimiter_discarded
