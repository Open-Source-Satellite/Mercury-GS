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
#  Mercury GS Protocol Formatting and Packet Handling
#  @author: Jamie Bayley (jbayley@kispe.co.uk)
###################################################################################
from low_level.serial_comms import frame_queue, serial_send
from low_level.frameformat import MessageFormat, DataType, struct, PROTOCOL_DELIMITER
from low_level.continuous import continuous_sender, register_continuous
import config
import threading


def packet_register_callback(tlm_function_ptr, tlm_rejection_function_ptr, tc_function_ptr, exception_handler_function_ptr):
    """ Registers the callbacks for this module to pass data back to previous modules. """
    global callback_telemetry_response
    global callback_telecommand_response
    global callback_exception_handler
    global callback_telemetry_rejection_response
    # Register telemetry response callback to pass telemetry packet up to module
    callback_telemetry_response = tlm_function_ptr
    # Register telemetry response callback to pass telemetry rejection packet up to module
    callback_telemetry_rejection_response = tlm_rejection_function_ptr
    # Register telecommand response callback to pass telecommand packet up to module
    callback_telecommand_response = tc_function_ptr
    # Register exception handler callback
    callback_exception_handler = exception_handler_function_ptr


class PacketHandler(threading.Thread):
    """ PacketHandler Class to handle incoming valid frames """

    def __init__(self, queue):
        """ Initialise Thread, set argument as frame_queue and start Thread"""
        super().__init__()
        self.args = queue
        self.start()

    def run(self):
        """ Waits for queue to be populated with a valid frame, then pops one off, picks bitfields out of frame
        and passes data up to correct module depending on data type field.
        """
        while True:
            # Wait for queue to contain a frame, pop one off
            frame = frame_queue.get()
            # Unpack bitfields
            frame_header_bytes = frame[:4]
            frame_data_type = frame[4]
            frame_data_length_bytes = frame[5:9]
            frame_data_length = struct.unpack("!L", frame_data_length_bytes)[0]
            frame_data_bytes = frame[9:]

            # Pass data field up to correct module depending on data type field
            if frame_data_type == DataType.TELEMETRY_DATA.value:
                callback_telemetry_response(frame_data_bytes)
            elif frame_data_type == DataType.TELEMETRY_REQUEST_REJECTION.value:
                callback_telemetry_rejection_response(frame_data_bytes)
            elif frame_data_type == DataType.TELECOMMAND_RESPONSE.value:
                callback_telecommand_response(frame_data_bytes)


def packet_init():
    """ Initialise Packet Handler class instance, which automatically starts the packet handler Thread. """
    global packet_handler
    packet_handler = PacketHandler(frame_queue)


def data_format(data_to_format, data_format_builder):
    """ Format data passed in in the format of the struct builder also passed in,
    return the formatted data.
    This function fulfills requirements PLAT_COMMS_00050 and PLAT_COMMS_00130.
    """
    formatted_data = data_format_builder.pack(*data_to_format)
    return formatted_data


def packetize(data_to_packet, data_type, is_continuous, message_object_database, latest_message_object):
    """ Format the data into the desired protocol
    This function fulfills requirement PLAT_COMMS_00040.
    """
    # Create class instance for the packet, this may be useful in the future
    packet_class = MessageFormat(data_to_packet, len(data_to_packet), data_type)
    # Create the packet builder using Struct module to build a packet binary representation of
    # 5 Individual Bytes followed by an Unsigned 32 Bit Int, Big Endian.
    packet_builder = struct.Struct("! 5B I")
    # Build the packet
    packet_packed = bytearray(packet_builder.pack(packet_class.header,
                                                  packet_class.reserved1,
                                                  packet_class.reserved2,
                                                  packet_class.reserved3,
                                                  packet_class.data_type,
                                                  packet_class.data_length))

    # Add the data field on the end of the packet
    # (this cannot be created using the packet builder as the data field is of variable size).
    packet_packed.extend(packet_class.data)
    # Scan the packet for delimiter bytes, add an extra delimiter after any delimiter found except the first one
    packet = delimiter_scan_and_add(packet_packed)
    # Start the Timeout timer for this message
    latest_message_object.start_timer()
    # Send the message
    serial_send(packet)

    if is_continuous is True:
        try:
            register_continuous(config.TC_TLM_RATE, continuous_sender, packet, message_object_database,
                                latest_message_object)
        except ZeroDivisionError as err:
            print("\n", repr(err))
            print("ERROR: Rate is 0, cannot run continuously")
            callback_exception_handler("ERROR: Rate is 0, cannot run continuously")


def delimiter_scan_and_add(data_to_scan):
    """ Scan data passed in for any delimiters,
    insert an extra delimiter after any delimiter found except the first one so that the receiver doesn't interpret
    it as a start of a new frame.
    This function fulfills requirement PLAT_COMMS_00045
    """
    # Copy data buffer into mutable bytearray
    data_editable_copy = bytearray(data_to_scan)
    header_checked = False
    num_added_delimiters = 0
    # Iterate over bytes in data
    for index, byte in enumerate(data_to_scan):
        if byte == PROTOCOL_DELIMITER:
            # This byte is a delimiter!
            if header_checked is False:
                # This is the first delimiter found, I.E Start of Frame. Do not add another delimiter after it.
                header_checked = True
            else:
                # Add another delimiter after this
                data_editable_copy.insert(index + num_added_delimiters, PROTOCOL_DELIMITER)
                num_added_delimiters += 1
                if index >= 9:
                    data_editable_copy[8] += 1 # TODO: Find a better solution, this will overflow after 255
                    # TODO: Also index of data length may not be 8 if there are delimiters in the header
    # Copy edited bytearray back over to data buffer and return
    scanned_data = bytes(data_editable_copy)
    return scanned_data
