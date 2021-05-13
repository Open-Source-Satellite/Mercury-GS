import config
import low_level


def register_callback(tlm_function_ptr, tc_function_ptr):
    global callback_telemetry_response
    global callback_telecommand_response
    callback_telemetry_response = tlm_function_ptr
    callback_telecommand_response = tc_function_ptr


def packet_init():
    low_level.register_callback(packet_init)


def packetize(data_to_packet):
    pass


def unpacketize(packet_to_data):
    callback_telemetry_response(packet_to_data)

