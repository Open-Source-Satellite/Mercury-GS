from low_level.serial_comms import frame_queue
import low_level.serial_comms
from low_level.frameformat import MessageFormat, DataType, struct
import threading
import config
from low_level.continuous import continuous_sender, register_continuous


def packet_register_callback(tlm_function_ptr, tc_function_ptr):
    global callback_telemetry_response
    global callback_telecommand_response
    callback_telemetry_response = tlm_function_ptr
    callback_telecommand_response = tc_function_ptr


def unpacketize(packet_to_data):
    frame_header_bytes = packet_to_data[:4]
    frame_data_type = packet_to_data[4]
    frame_data_length_bytes = packet_to_data[5:9]
    frame_data_length = struct.unpack("!L", frame_data_length_bytes)[0]
    frame_data_bytes = packet_to_data[9:]
    # frame_data = int.from_bytes(frame_data_bytes, "big")

    if frame_data_type == DataType.TELEMETRY_DATA.value:
        callback_telemetry_response(frame_data_bytes)
    elif frame_data_type == DataType.TELECOMMAND_RESPONSE.value:
        callback_telecommand_response(frame_data_bytes)


def packet_init():
    if not rx_packet_handler_thread.is_alive():
        rx_packet_handler_thread.start()


def packet_handler():
    while True:
        frame = frame_queue.get()
        unpacketize(frame)


rx_packet_handler_thread = threading.Thread(target=packet_handler, args=())


def data_format(data_to_format, data_format_builder):
    formatted_data = data_format_builder.pack(*data_to_format)
    return formatted_data


def packetize(data_to_packet, data_type, is_continuous, message_object_database, latest_message_object):
    packet_class = MessageFormat(data_to_packet, len(data_to_packet), data_type)
    packet_builder = struct.Struct("! 5B I")
    packet_packed = bytearray(packet_builder.pack(packet_class.header,
                                                  packet_class.reserved1,
                                                  packet_class.reserved2,
                                                  packet_class.reserved3,
                                                  packet_class.data_type,
                                                  packet_class.data_length))

    packet_packed.extend(packet_class.data)

    packet = x55_scan(packet_packed)
    latest_message_object.start_timer()
    low_level.serial_comms.serial_handler.serial.send(packet)

    if is_continuous is True:
        try:
            register_continuous(config.TC_TLM_RATE, continuous_sender, packet, message_object_database,
                                latest_message_object)
        except ZeroDivisionError as err:
            print("\n", repr(err))
            print("ERROR: Rate is 0, cannot run continuously")


def x55_scan(data_to_scan):
    data_list = list(data_to_scan)
    header_checked = False
    for index, byte in enumerate(data_to_scan):
        if byte == 0x55:
            if header_checked is False:
                header_checked = True
            else:
                data_list.insert(index, 0x55)

    data_to_scan = bytes(data_list)
    return data_to_scan
