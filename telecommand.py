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
from packet import packetize, DataType, data_format, struct
from serial_framing.frameformat import telecommand_request_builder_string, telecommand_request_builder_integer, \
    telecommand_request_builder_float


def telecommand_register_callback(tc_update_function_ptr):
    global callback_telecommand_response_update
    callback_telecommand_response_update = tc_update_function_ptr


def tc_request_send(telecommand_number, telecommand_data, telecommand_data_type):
    try:
        if telecommand_data_type == "String":
            # Prepend whitespace until string is 8 chars
            while len(telecommand_data) < 8:
                telecommand_data = " " + telecommand_data
            # Format the data as an 8 byte string
            data = data_format([int(telecommand_number), *bytes(telecommand_data, "ascii")],
                               telecommand_request_builder_string)
        try:
            if telecommand_data_type == "Integer" and telecommand_data:
                # Format the data as a 64 bit signed integer
                data = data_format([int(telecommand_number), int(telecommand_data)],
                                   telecommand_request_builder_integer)
        except ValueError as err:
            # Handle exception if data is not an integer
            print("ERROR: ", err)
            print("Telecommand Data value is not Integer")
        try:
            if telecommand_data_type == "Floating Point":
                # Format the data as a double
                data = data_format([int(telecommand_number), float(telecommand_data)],
                                   telecommand_request_builder_float)
        except ValueError as err:
            # Handle exception if data is not a float
            print("ERROR: ", err)
            print("Telecommand Data value is not Floating Point Number")
            # Format the telecommand as a frame and send
            packetize(data, DataType.TELECOMMAND_REQUEST.value)
    except UnboundLocalError as err:
        print("ERROR: ", err)
        print("Could not format message")
    except ValueError as err:
        print("ERROR: ", err)
        print("Telecommand Request Channel is invalid")


def tc_response(telecommand_packet):
    pass
