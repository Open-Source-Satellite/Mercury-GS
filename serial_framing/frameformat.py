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
#  OSSAT Platform Comms message frame format
#  @author: Ricardo Mota (ricardoflmota@gmail.com)
###################################################################################
from enum import Enum
import struct

PROTOCOL_DELIMITER = 0x55
RESERVED = bytearray.fromhex("DE AD BE")
MAX_DATA_TYPES = 6

telecommand_request_builder = struct.Struct("! I 8B")
telecommand_response_builder = struct.Struct("! I B")
telemetry_request_builder = struct.Struct("! I")
telemetry_response_builder = struct.Struct("! I Q")


class MessageFormat:
    header = PROTOCOL_DELIMITER
    reserved1 = RESERVED[0]
    reserved2 = RESERVED[1]
    reserved3 = RESERVED[2]

    def __init__(self, message_data, message_data_length, message_data_type):
        self.data_length = message_data_length
        self.data_type = message_data_type
        self.data = message_data


class DataType(Enum):
    TELECOMMAND_REQUEST = 0x01
    TELECOMMAND_RESPONSE = 0x02
    TELEMETRY_DATA = 0x03
    TELEMETRY_REQUEST = 0x04
    FILE_UPLOAD = 0x05
    FILE_DOWNLOAD = 0x06
    TELEMETRY_REQUEST_REJECTION = 0x07


class TelecommandResponseState(Enum):
    SUCCESS = 0x00
    FAILED = 0x01
    INVALID_LENGTH = 0x02
    COMMAND_NOT_SUPPORTED = 0x03
    INVALID_COMMAND_ARGUMENT = 0x04


class TelemetryResponseState(Enum):
    SUCCESS = 0x00
    FAILED = 0x01
