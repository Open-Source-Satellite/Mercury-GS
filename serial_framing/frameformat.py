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

from construct import *

PROTOCOL_HEADER = 0x55

telecommand_request_format = Struct(
    "telecommand_number" / Int32ub,
    "telecommand_data" / Array(8, Byte),
)

telecommand_response = Enum(Byte,
                            SUCCESS=0x00,
                            FAILED=0x01,
                            INVALID_CMD=0x02,
                            )

data_type = Enum(Byte,
                 TELECOMMAND_REQUEST=0x01,
                 TELECOMMAND_RESPONSE=0x02,
                 TELEMETRY_DATA=0x03,
                 TELEMETRY_REQUEST=0x04,
                 FILE_UPLOAD=0x05,
                 FILE_DOWNLOAD=0x06,
                 __default__=Pass,
                 )

telecommand_response_format = Struct(
    "telecommand_number" / Int32ub,
    "telecommand_response" / telecommand_response,
)

message_format = Struct(
    "header" / Const(b'\x55'),
    "reserved" / Array(3, Byte),
    "data_type" / data_type,
    "data_length" / Int32ub,
    "data" / Array(this.data_length, Byte)
)

# %%
if __name__ == "__main__":

    container = Container(
        header=b'\x55',
        reserved=[0x55, 0x69, 0x96],
        data_type="TELEMETRY_DATA",
        data_length=4,
        data=[0xDE, 0xAD, 0xBE, 0xEF],
    )

    print(container)

    raw_msg = message_format.build(container)

    print(raw_msg.hex())
