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
from flask_restful import fields, marshal_with, reqparse, Resource
from threading import Timer
from api.resources.low_level.packet import packetize, DataType, data_format
from api.resources.low_level.frameformat import telemetry_request_builder, telemetry_response_builder

telemetry_database = []

post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'tlm_channel', dest='tlm_channel',
    type=int, location='form', 
    required=True,
    help='The telemetry channel',
)
post_parser.add_argument(
    'tc_timeout', dest='tc_timeout',
    type=int, location='form',
    default=1000,
    help='The telemetry timeout (optional)',
)
post_parser.add_argument(
    'is_continuous', dest='is_continuous',
    type=bool, location='form',
    default=False,
    help='The telemetry is_continue param (default: False)',
)

telemetry_fields = {
    'tlm_channel': fields.Integer,
    'tc_timeout': fields.Integer,
    'is_continuous': fields.Boolean
}

class Telemetry(Resource):
    @marshal_with(telemetry_fields)
    def __init__(self, **kwargs):
        args = post_parser.parse_args()
        self.ID = args.tlm_channel
        self.TimeoutTimer = Timer(
            args.tc_timeout,
            self.timeout
        )
        self.is_continuous = args.is_continuous

    def post(self):
        self.tlm_request_send(self.ID, self.is_continuous)

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
                                 not self.tlm_search_for_id_match(self.ID)]
        # Increment the timeout counter
        # callback_telemetry_timeout()

    def tlm_request_send(self, is_continuous: bool):
        """ Check data type of Telemetry Request before formatting and send over COM Port. """
        try:
            # Add telemetry message to database to enable matching with response
            telemetry_database.append((int(self.ID), config.TIMEOUT))
            # Format the telemetry request as a frame and send
            data = data_format([int(self.ID)], telemetry_request_builder)
            packetize(data, DataType.TELEMETRY_REQUEST.value, is_continuous, telemetry_database, telemetry_database[-1])
        except UnboundLocalError as err:
            print("ERROR: ", err)
            print("INFO: Could not format message")
            # callback_exception_handler("ERROR: Could not format message")
        except ValueError as err:
            print("ERROR: ", err)
            print("INFO: Telemetry Request Channel is invalid")
            # callback_exception_handler("ERROR: Telemetry Request Channel is invalid")

    def tlm_search_for_id_match(self, id_to_match, action=None):
        """ If the ID matches return True, stop the timer if action = "STOP_TIMEOUT". """
        if self.ID == id_to_match:
            if action == "STOP_TIMEOUT":
                self.stop_timer()
            return True
        else:
            return False


    def tlm_response(self, telemetry_packet):
        """ Telemetry Response received, unpack the bitfields and stop the timeout timer for this message,
        then pass the response up to the GUI to display.
        """
        # Unpack the packet into bitfields
        telemetry_response = telemetry_response_builder.unpack(telemetry_packet)
        # TODO: struct.error, unpack requires a buffer of 12 bytes. check data length
        tlm_channel = telemetry_response[0]
        # Not being use for now as the callback is commented out
        tlm_data = telemetry_response[1]

        # Search for the first element of the database where the ID matches, remove it and stop the associated timeout timer
        telemetry_database[:] = [telemetry for telemetry in telemetry_database if
                                not self.tlm_search_for_id_match(tlm_channel, "STOP_TIMEOUT")]

        # Pass the data back up to the GUI to display
        # callback_telemetry_response_update(str(tlm_channel), str(tlm_data))
