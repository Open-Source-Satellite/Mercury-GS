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

import packet
import low_level

def register_callback(tlm_update_function_ptr):
    global callback_telemetry_response_update
    callback_telemetry_response_update = tlm_update_function_ptr


def tlm_request_send():
    TLM_REQUEST = "TEST"
    low_level.send(TLM_REQUEST)


def tlm_response(telemetry_packet):
    callback_telemetry_response_update(telemetry_packet)