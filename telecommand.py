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
from config import TIMEOUT
from low_level.packet import packetize, DataType, data_format
from low_level.frameformat import telecommand_request_builder_string, telecommand_request_builder_integer, \
    telecommand_request_builder_float, telecommand_response_builder, TelecommandResponseState
from threading import Timer

telecommand_database = []


class Telecommand:
    def __init__(self, number, tc_timeout):
        self.ID = number
        self.TimerFunction = Timer(tc_timeout, self.timeout)

    def start_timer(self):
        self.TimerFunction.start()

    def stop_timer(self):
        self.TimerFunction.cancel()

    def timeout(self):
        telecommand_database[:] = [telecommand for telecommand in telecommand_database if
                                   not tc_search_for_id_match(telecommand, self.ID)]
        callback_telecommand_timeout()


def telecommand_register_callback(tc_update_function_ptr, tc_timeout_function_ptr):
    global callback_telecommand_response_update
    global callback_telecommand_timeout
    callback_telecommand_response_update = tc_update_function_ptr
    callback_telecommand_timeout = tc_timeout_function_ptr


def tc_request_send(telecommand_number, telecommand_data, telecommand_data_type, is_continuous):
    try:
        telecommand_number = int(telecommand_number)
    except ValueError as err:
        print(str(repr(err)))
        print("ERROR: Telecommand Request Channel is invalid")

    try:
        if telecommand_data_type == "String":
            # Prepend whitespace until string is 8 chars
            while len(telecommand_data) < 8:
                telecommand_data = " " + telecommand_data
            # Format the data as an 8 byte string
            data = data_format([telecommand_number, *bytes(telecommand_data, "ascii")],
                               telecommand_request_builder_string)
        try:
            if telecommand_data_type == "Integer":
                # Format the data as a 64 bit signed integer
                data = data_format([telecommand_number, int(telecommand_data)],
                                   telecommand_request_builder_integer)
        except ValueError as err:
            # Handle exception if data is not an integer
            print(repr(err))
            print("ERROR: Telecommand Data value is not Integer")
        try:
            if telecommand_data_type == "Floating Point":
                # Format the data as a double
                data = data_format([telecommand_number, float(telecommand_data)],
                                   telecommand_request_builder_float)
        except ValueError as err:
            # Handle exception if data is not a float
            print(repr(err))
            print("ERROR: Telecommand Data value is not Floating Point Number")

        # Format the telecommand as a frame and send
        telecommand_database.append(Telecommand(telecommand_number, TIMEOUT))
        packetize(data, DataType.TELECOMMAND_REQUEST.value, is_continuous, telecommand_database, telecommand_database[-1])
    except UnboundLocalError as err:
        print(repr(err))
        print("ERROR: Could not format message")


def tc_search_for_id_match(telecommand, id_to_match, action=None):
    if telecommand.ID == id_to_match:
        if action == "STOP_TIMEOUT":
            telecommand.stop_timer()
        return True
    else:
        return False


def tc_response(telecommand_packet):
    telecommand_data = telecommand_response_builder.unpack(telecommand_packet)
    telecommand_number = telecommand_data[0]
    telecommand_response = telecommand_data[1]

    telecommand_database[:] = [telecommand for telecommand in telecommand_database if
                               not tc_search_for_id_match(telecommand, telecommand_number, "STOP_TIMEOUT")]

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

    callback_telecommand_response_update(str(telecommand_number), telecommand_response_status)



