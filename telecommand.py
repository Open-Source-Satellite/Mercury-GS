###################################################################################
# @file telecommand.py
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
#  Mercury GS Telecommand Handler
#  @author: Jamie Bayley (jbayley@kispe.co.uk)
###################################################################################
import struct
import config
from low_level.packet import packetize, DataType, data_format
from low_level.frameformat import telecommand_request_builder_string, telecommand_request_builder_integer, \
    telecommand_request_builder_float, telecommand_response_builder, telecommand_time_builder_string, TelecommandResponseState
from threading import Timer

telecommand_database = []


class Telecommand:  # A Class for each Telecommand
    """ The Telecommand Class. """

    def __init__(self, number, tc_timeout):
        """ Init Function, Sets the Telecommand Request Number,
        creates instance of Timer to handle Timeouts using the  Timeout value.
        """
        self.ID = number
        self.TimeoutTimer = Timer(tc_timeout, self.timeout)

    def start_timer(self):
        """ Start the timeout timer. """
        self.TimeoutTimer.start()

    def stop_timer(self):
        """ Stop the timeout timer. """
        self.TimeoutTimer.cancel()

    def timeout(self):
        """ Called if the timeout timer executes (has timed out). """
        # Search for the first element of the database where the ID matches and remove it
        telecommand_database[:] = [telecommand for telecommand in telecommand_database if
                                   not tc_search_for_id_match(telecommand, self.ID)]
        # Increment the timeout counter
        callback_telecommand_timeout()


def telecommand_register_callback(tc_update_function_ptr, tc_timeout_function_ptr, exception_handler_function_ptr):
    """ Registers the callbacks for this module to pass data back to previous modules. """
    global callback_telecommand_response_update
    global callback_telecommand_timeout
    global callback_exception_handler
    # Register callback for updating the GUI with a telecommand response
    callback_telecommand_response_update = tc_update_function_ptr
    # Register callback for updating timeout counter when a telecommand request timeouts
    callback_telecommand_timeout = tc_timeout_function_ptr
    # Set exception handler callback
    callback_exception_handler = exception_handler_function_ptr


def tc_request_send(telecommand_number, telecommand_data, telecommand_data_type, is_continuous):
    """ Check data type of Telecommand Request before formatting and send over COM Port. """
    try:
        type_error = ""
        telecommand_number = int(telecommand_number)
    except ValueError as err:
        print(str(repr(err)))
        print("ERROR: Telecommand Request Channel is invalid")
        callback_exception_handler("Telecommand Request Channel is invalid")

    try:
        if telecommand_data_type == "String":
            # Prepend whitespace until string is 8 chars
            while len(telecommand_data) < 8:
                telecommand_data = " " + telecommand_data
            # Format the data as an 8 byte string
            data = data_format([telecommand_number, *bytes(telecommand_data, "ascii")],
                               telecommand_request_builder_string)
    except struct.error as err:
        print(repr(err))
        print("ERROR: Telecommand Data Value is not String")
        type_error = "Telecommand Data Value is not String"
    try:
        if telecommand_data_type == "Integer":
            # Format the data as a 64 bit signed integer
            data = data_format([telecommand_number, int(telecommand_data)],
                               telecommand_request_builder_integer)
    except ValueError as err:
        # Handle exception if data is not an integer
        print(repr(err))
        print("ERROR: Telecommand Data Value is not Integer")
        type_error = "Telecommand Data Value is not Integer"
    try:
        if telecommand_data_type == "Floating Point":
            # Format the data as a double
            data = data_format([telecommand_number, float(telecommand_data)],
                               telecommand_request_builder_float)
    except ValueError as err:
        # Handle exception if data is not a float
        print(repr(err))
        print("ERROR: Telecommand Data Value is not Floating Point Number")
        type_error = "Telecommand Data Value is not Floating Point Number"

    try:
        # Add telecommand message to database to enable matching with response
        telecommand_database.append(Telecommand(telecommand_number, config.TIMEOUT))
        # Format the telecommand as a frame and send
        packetize(data, DataType.TELECOMMAND_REQUEST.value, is_continuous, telecommand_database,
                  telecommand_database[-1])
    except UnboundLocalError as err:
        print(repr(err))
        print("ERROR: Could not format message")
        callback_exception_handler("ERROR: Could not format message, " + type_error)


def tc_search_for_id_match(telecommand, id_to_match, action=None):
    """ If the ID matches return True, stop the timer if action = "STOP_TIMEOUT". """
    if telecommand.ID == id_to_match:
        if action == "STOP_TIMEOUT":
            telecommand.stop_timer()
        return True
    else:
        return False


def tc_response(telecommand_packet):
    """ Telecommand Response received, unpack the bitfields and stop the timeout timer for this message,
    then pass the response up to the GUI to display.
    """
    # Unpack the packet into bitfields
    telecommand_data = telecommand_response_builder.unpack(telecommand_packet)
    telecommand_number = telecommand_data[0]
    telecommand_response = telecommand_data[1]

    # Search for the first element of the database where the ID matches, remove it and stop the associated timeout timer
    telecommand_database[:] = [telecommand for telecommand in telecommand_database if
                               not tc_search_for_id_match(telecommand, telecommand_number, "STOP_TIMEOUT")]

    # Get the telecommand response status value
    if telecommand_response == TelecommandResponseState.SUCCESS.value:
        telecommand_response_status = TelecommandResponseState.SUCCESS.name
    elif telecommand_response == TelecommandResponseState.FAILED.value:
        telecommand_response_status = TelecommandResponseState.FAILED.name
    elif telecommand_response == TelecommandResponseState.INVALID_LENGTH.value:
        telecommand_response_status = TelecommandResponseState.INVALID_LENGTH.name
    elif telecommand_response == TelecommandResponseState.COMMAND_NOT_SUPPORTED.value:
        telecommand_response_status = TelecommandResponseState.COMMAND_NOT_SUPPORTED.name
    elif telecommand_response == TelecommandResponseState.INVALID_COMMAND_ARGUMENT.value:
        telecommand_response_status = TelecommandResponseState.INVALID_COMMAND_ARGUMENT.name

    # Pass the status back up to the GUI to display
    callback_telecommand_response_update(str(telecommand_number), telecommand_response_status)

def tc_time_send(telecommand_number, unix_time_string):
    try:
        while len(unix_time_string) < 2:
            unix_time_string = " " + unix_time_string
            unix_time_string = data_format([telecommand_number, *bytes(unix_time_string, "ascii")],
                                        telecommand_time_builder_string)
    except struct.error as err:
        print(repr(err))
        print("ERROR: Telecommand Time is not String")
        type_error = "Telecommand Time is not String"

    try:
        # Add telecommand time to database to enable matching with response
        telecommand_database.append(Telecommand(telecommand_number, config.TIMEOUT))
        # Format the telecommand as a frame and send.
        # is_continious is set to 0.
        packetize(unix_time_string, DataType.TELECOMMAND_REQUEST.value, 0 , telecommand_database,
                  telecommand_database[-1])
    except UnboundLocalError as err:
        print(repr(err))
        print("ERROR: Could not format message")
        callback_exception_handler("ERROR: Could not format message, " + type_error)

