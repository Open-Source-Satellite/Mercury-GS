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
import config
from threading import Timer
from low_level.packet import packetize, DataType, data_format
from low_level.frameformat import telemetry_request_builder, telemetry_response_builder

telemetry_database = []


class Telemetry:
    """ The Telemetry Class. """

    def __init__(self, number, tc_timeout):
        """ Init Function, Sets the Telemetry Request Number,
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
        telemetry_database[:] = [telemetry for telemetry in telemetry_database if
                                 not tlm_search_for_id_match(telemetry, self.ID)]
        # Increment the timeout counter
        callback_telemetry_timeout()


def telemetry_register_callback(tlm_update_function_ptr, tlm_timeout_function_ptr, exception_handler_function_ptr):
    """ Registers the callbacks for this module to pass data back to previous modules. """
    global callback_telemetry_response_update
    global callback_telemetry_timeout
    global callback_exception_handler
    # Register callback for updating the GUI with a telemetry response
    callback_telemetry_response_update = tlm_update_function_ptr
    # Register callback for updating timeout counter when a telemetry request timeouts
    callback_telemetry_timeout = tlm_timeout_function_ptr
    # Set exception handler callback
    callback_exception_handler = exception_handler_function_ptr


def tlm_request_send(tlm_channel, is_continuous):
    """ Check data type of Telemetry Request before formatting and send over COM Port. """
    try:
        # Add telemetry message to database to enable matching with response
        telemetry_database.append(Telemetry(int(tlm_channel), config.TIMEOUT))
        # Format the telemetry request as a frame and send
        data = data_format([int(tlm_channel)], telemetry_request_builder)
        packetize(data, DataType.TELEMETRY_REQUEST.value, is_continuous, telemetry_database, telemetry_database[-1])
    except UnboundLocalError as err:
        print("ERROR: ", err)
        print("INFO: Could not format message")
        callback_exception_handler("ERROR: Could not format message")
    except ValueError as err:
        print("ERROR: ", err)
        print("INFO: Telemetry Request Channel is invalid")
        callback_exception_handler("ERROR: Telemetry Request Channel is invalid")


def tlm_search_for_id_match(telemetry, id_to_match, action=None):
    """ If the ID matches return True, stop the timer if action = "STOP_TIMEOUT". """
    if telemetry.ID == id_to_match:
        if action == "STOP_TIMEOUT":
            telemetry.stop_timer()
        return True
    else:
        return False


def tlm_response(telemetry_packet):
    """ Telemetry Response received, unpack the bitfields and stop the timeout timer for this message,
    then pass the response up to the GUI to display.
    """
    # Unpack the packet into bitfields
    telemetry_response = telemetry_response_builder.unpack(telemetry_packet)
    tlm_channel = telemetry_response[0]
    tlm_data = telemetry_response[1]

    # Search for the first element of the database where the ID matches, remove it and stop the associated timeout timer
    telemetry_database[:] = [telemetry for telemetry in telemetry_database if
                             not tlm_search_for_id_match(telemetry, tlm_channel, "STOP_TIMEOUT")]

    # Pass the data back up to the GUI to display
    callback_telemetry_response_update(tlm_channel, str(tlm_data))
