# %%
from construct import *

# message_crc = Struct('message_crc', ULInt32('crc'))

PROTOCOL_DELIMITER = 0x55

# %%
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
    "header" / Const(PROTOCOL_DELIMITER),
    "reserved" / Array(3, Byte),
    "data_type" / data_type,
    "data_length" / Int32ub,
    "data" / Array(this.data_length, Byte)
)

# %%
if __name__ == "__main__":

    container = Container(
        header=PROTOCOL_DELIMITER,
        reserved=[0x55, 0x69, 0x96],
        data_type="TELEMETRY_DATA",
        data_length=4,
        data=[0xDE, 0xAD, 0xBE, 0xEF],
    )

    print(container)

    raw_msg = message_format.build(container)

    print(raw_msg.hex())

    # raw = message_format.build(Container(
    #     msg_id=0x1234,
    #     dest_addr=0xacba,
    #     command_type='RESTART',
    #     flags=Container(on=1, cache=0, status=4),
    #     datalen=4,
    #     data=[0x1, 0xff, 0xff, 0xdd],
    #     crc=0x12345678))

    # print(raw.encode('hex'))

# %%
