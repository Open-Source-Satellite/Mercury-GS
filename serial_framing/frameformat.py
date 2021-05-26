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

PROTOCOL_DELIMITER = 0x55
RESERVED = [0xDE, 0xAD, 0xBE]
MAX_DATA_TYPES = 6


class MessageFormat:
    header = PROTOCOL_DELIMITER
    reserved1 = RESERVED[0]
    reserved2 = RESERVED[1]
    reserved3 = RESERVED[2]

    def __init__(self, data, data_length, data_type):
        self.data_length = data_length
        self.data_type = data_type
        self.data = data


class DataType(Enum):
    TELECOMMAND_REQUEST = 0x01
    TELECOMMAND_RESPONSE = 0x02
    TELEMETRY_DATA = 0x03
    TELEMETRY_REQUEST = 0x04
    FILE_UPLOAD = 0x05
    FILE_DOWNLOAD = 0x06

class telecommand_request_format():
    pass

# "telecommand_number" / Int32ub,
# "telecommand_data" / Array(8, Byte),


class telecommand_response(Enum):
    SUCCESS = 0x00
    FAILED = 0x01
    INVALID_CMD = 0x02


class telecommand_response_format():
    pass

# "telecommand_number" / Int32ub,
# "telecommand_response" / telecommand_response,

# %%
if __name__ == "__main__":
    header = b'\x55'
    reserved = [0x55, 0x69, 0x96]
    data_type = "TELEMETRY_DATA"
    data_length = 4
    data = [0xDE, 0xAD, 0xBE, 0xEF]
