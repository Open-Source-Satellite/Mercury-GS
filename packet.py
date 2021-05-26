from low_level import frame_queue, send, register_callback
from serial_framing.frameformat import MessageFormat, DataType
import struct
import threading


def register_callback(tlm_function_ptr, tc_function_ptr):
    global callback_telemetry_response
    global callback_telecommand_response
    callback_telemetry_response = tlm_function_ptr
    callback_telecommand_response = tc_function_ptr


def unpacketize(packet_to_data):
    frame_header_bytes = packet_to_data[:4]
    frame_data_type_bytes = packet_to_data[4]
    frame_data_length_bytes = packet_to_data[5:9]
    frame_data_length = struct.unpack("!L", b"".join(frame_data_length_bytes))[0]
    frame_data_bytes = packet_to_data[9:]
    frame_data = int.from_bytes(frame_data_bytes[0], "little")

    callback_telemetry_response(str(frame_data))


def packet_init():
    register_callback(packet_init, packet_handler)


def packet_handler_thread_start():
    if not rx_packet_handler_thread.is_alive():
        rx_packet_handler_thread.start()


def packet_handler():
    while frame_queue.qsize() > 0:
        frame = frame_queue.get()
        unpacketize(frame)


rx_packet_handler_thread = threading.Thread(target=packet_handler, args=())


def packetize(data_to_packet, data_type):
    packet_class = MessageFormat(data_to_packet, len(data_to_packet), data_type)
    packet_builder = struct.Struct("! 5B I")
    packet_packed = bytearray(packet_builder.pack(packet_class.header,
                                                  packet_class.reserved1,
                                                  packet_class.reserved2,
                                                  packet_class.reserved3,
                                                  packet_class.data_type,
                                                  packet_class.data_length))

    packet_packed.append(int(packet_class.data))

    packet = x55_scan(bytearray(packet_packed))
    send(packet)


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
