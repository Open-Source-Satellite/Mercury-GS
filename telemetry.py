###################################################################################
# @file telemetry.py
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
#  Mercury GS Telemetry Handler
#  @author: Jamie Bayley (jbayley@kispe.co.uk)
###################################################################################

from low_level.packet import packetize, DataType, data_format
from low_level.frameformat import telemetry_request_builder, telemetry_response_builder


def telemetry_register_callback(tlm_update_function_ptr):
    global callback_telemetry_response_update
    callback_telemetry_response_update = tlm_update_function_ptr


def tlm_request_send(tlm_channel, is_continuous):
    try:
        data = data_format([tlm_channel], telemetry_request_builder)
        packetize(data, DataType.TELEMETRY_REQUEST.value, is_continuous)
    except UnboundLocalError as err:
        print("ERROR: ", err)
        print("INFO: Could not format message")
    except ValueError as err:
        print("ERROR: ", err)
        print("INFO: Telemetry Request Channel is invalid")


def tlm_response(telemetry_packet):
    telemetry_response = telemetry_response_builder.unpack(telemetry_packet)
    tlm_channel = telemetry_response[0]
    tlm_data = telemetry_response[1]
    callback_telemetry_response_update(tlm_channel, str(tlm_data))
