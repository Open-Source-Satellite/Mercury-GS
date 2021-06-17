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
from config import TIMEOUT
from threading import Timer
from low_level.packet import packetize, DataType, data_format
from low_level.frameformat import telemetry_request_builder, telemetry_response_builder

telemetry_database = []


class Telecommand:
    def __init__(self, number, tc_timeout):
        self.ID = number
        self.TimerFunction = Timer(tc_timeout, self.timeout)

    def start_timer(self):
        self.TimerFunction.start()

    def stop_timer(self):
        self.TimerFunction.cancel()

    def timeout(self):
        telemetry_database[:] = [telemetry for telemetry in telemetry_database if
                                 not tlm_search_for_id_match(telemetry, self.ID)]
        callback_telemetry_timeout()


def telemetry_register_callback(tlm_update_function_ptr, tlm_timeout_function_ptr):
    global callback_telemetry_response_update
    global callback_telemetry_timeout
    callback_telemetry_response_update = tlm_update_function_ptr
    callback_telemetry_timeout = tlm_timeout_function_ptr


def tlm_request_send(tlm_channel, is_continuous):
    try:
        # Format the telemetry request as a frame and send
        telemetry_database.append(Telecommand(tlm_channel, TIMEOUT))
        data = data_format([int(tlm_channel)], telemetry_request_builder)
        packetize(data, DataType.TELEMETRY_REQUEST.value, is_continuous, telemetry_database, telemetry_database[-1])
    except UnboundLocalError as err:
        print("ERROR: ", err)
        print("INFO: Could not format message")
    except ValueError as err:
        print("ERROR: ", err)
        print("INFO: Telemetry Request Channel is invalid")


def tlm_search_for_id_match(telemetry, id_to_match, action=None):
    if telemetry.ID == id_to_match:
        if action == "STOP_TIMEOUT":
            telemetry.stop_timer()
        return True
    else:
        return False


def tlm_response(telemetry_packet):
    telemetry_response = telemetry_response_builder.unpack(telemetry_packet)
    tlm_channel = telemetry_response[0]
    tlm_data = telemetry_response[1]
    callback_telemetry_response_update(tlm_channel, str(tlm_data))
