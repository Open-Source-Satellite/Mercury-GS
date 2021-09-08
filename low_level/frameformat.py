###################################################################################
# @file frameformat.py
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
#  Created on: 17-Aug-2020
#  OSSAT Platform Comms Protocol Frame Format
#  @author: Ricardo Mota (ricardoflmota@gmail.com)
###################################################################################
from enum import Enum
import struct

PROTOCOL_DELIMITER = 0x55
RESERVED = bytearray.fromhex("DE AD BE")
MAX_DATA_TYPES = 8

""" Struct module Builders for message formatting. """
telecommand_request_builder_string = struct.Struct("! I 8B")
telecommand_request_builder_integer = struct.Struct("! I q")
telecommand_request_builder_float = struct.Struct("! I d")
telecommand_response_builder = struct.Struct("! I B")
telemetry_request_builder = struct.Struct("! I")
telemetry_response_builder = struct.Struct("! I Q")
telemetry_rejection_response_builder = struct.Struct("! I B")


class MessageFormat:
    """ MessageFormat class to set the bitfields for each message"""
    header = PROTOCOL_DELIMITER
    reserved1 = RESERVED[0]
    reserved2 = RESERVED[1]
    reserved3 = RESERVED[2]

    def __init__(self, message_data, message_data_length, message_data_type):
        self.data_length = message_data_length
        self.data_type = message_data_type
        self.data = message_data


class DataType(Enum):
    """ DataType class for each possible data type. """
    TELECOMMAND_REQUEST = 0x01
    TELECOMMAND_RESPONSE = 0x02
    TELEMETRY_DATA = 0x03
    TELEMETRY_REQUEST = 0x04
    FILE_UPLOAD = 0x05
    FILE_DOWNLOAD = 0x06
    TELEMETRY_REQUEST_REJECTION = 0x07


class DataTypeSize(Enum):
    """ DataType class for each possible data type. """
    TELECOMMAND_REQUEST = 12
    TELECOMMAND_RESPONSE = 5
    TELEMETRY_DATA = 12
    TELEMETRY_REQUEST = 4
    FILE_UPLOAD = 0x05
    FILE_DOWNLOAD = 0x06
    TELEMETRY_REQUEST_REJECTION = 0x07


class TelecommandResponseState(Enum):
    """ TelecommandResponseState class for each possible response state. """
    SUCCESS = 0x00
    FAILED = 0x01
    INVALID_LENGTH = 0x02
    COMMAND_NOT_SUPPORTED = 0x03
    INVALID_COMMAND_ARGUMENT = 0x04


class TelemetryRejectionResponseState(Enum):
    """ TelemetryResponseState class for each possible response state. """
    CHANNEL_NOT_SUPPORTED = 0x00
    INVALID_DATA_LENGTH = 0x01
