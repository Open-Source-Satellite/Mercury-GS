###################################################################################
# @file comms.py
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
#  Mercury GS Serial Driver
#  @author: Jamie Bayley (jbayley@kispe.co.uk)
###################################################################################
import queue
import struct
import threading
from enum import Enum

import serial
import config
from low_level.frameformat import PROTOCOL_DELIMITER, MAX_DATA_TYPES, DataType, DataTypeSize
from config import RaspberryPi
try:
    # If this succeeds then we are using a Raspberry Pi
    from config import GPIO
except ImportError:
    pass

import adafruit_rfm69
import sys
import signal


if RaspberryPi is True:
    try:
        import board as bonnet
        import busio
        from digitalio import DigitalInOut, Direction, Pull
        # Configure Packet Radio
        CS = DigitalInOut(bonnet.CE1)
        RESET = DigitalInOut(bonnet.D25)
        spi = busio.SPI(bonnet.SCK, MOSI=bonnet.MOSI, MISO=bonnet.MISO)
    except (NotImplementedError, NameError) as err:
        print(repr(err))
        #spi = None
        #CS = None
        #RESET = None

frame_queue = queue.Queue()
direct_read_queue = queue.Queue()
incoming_byte_queue = queue.Queue()
comms_handler = None
PENDING_FRAME = 0
GATHERING_DATA = 1
READING_DATA = 2
DIRECT_READ = 3
DIO0_GPIO = 22


def signal_handler(sig, frame):
    if RaspberryPi is True:
        GPIO.cleanup()
    sys.exit(0)


def comms_register_callback(exception_handler_function_ptr):
    """ Registers the callbacks for this module to pass data back to previous modules. """
    global callback_exception_handler
    # Set exception handler callback
    callback_exception_handler = exception_handler_function_ptr


class CommsHandler:
    """ A Class to handle the comms and rx_state_machine. """

    def __init__(self, port, baud_rate):
        """ Initialise the rx_listener and serial. """
        self.rx_state_machine = StateMachine()
        if RaspberryPi is True:
            self.radio = RadioComms(spi, CS, RESET, 434.0)
        self.serial = SerialComms(config.COM_PORT, config.BAUD_RATE)


class RadioComms(adafruit_rfm69.RFM69):
    """ A Class to handle the radio comms. """

    def __init__(self, spi, chip_select, reset, frequency):
        super().__init__(spi, chip_select, reset, frequency)
        self.encryption_key = b'\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08'
        self.is_open = True  # Hack JPB
        self.in_waiting = 0  # Hack JPB
        self.listen()

    def rx_interrupt(self, channel):
        received_packet = self.receive(timeout=10)
        if received_packet is not None:
            print("RECEIVED: " + str(received_packet))
            frame_queue.put(received_packet)
            # packet_split = struct.unpack(str(len(received_packet)) + "c", received_packet)
            # for byte in packet_split:
            # incoming_byte_queue.put(byte)


class SerialComms(serial.Serial):
    """ A Class to handle the serial comms through a UART. """

    def __init__(self, port, baud_rate):
        """ Initialise serial interface, set bytesize and write_timeout values. """
        try:
            super().__init__(port, baud_rate)
        except serial.serialutil.SerialException as err:
            print(repr(err))

        self.bytesize = 8
        self.write_timeout = 5
        self.rx_thread = threading.Thread(target=self.rx_loop)

        # Close COM Port if open
        if self.is_open:
            self.close()

        # Open COM Port
        try:
            self.open()
            self.rx_thread.start()
        except serial.serialutil.SerialException as err:
            print(repr(err))

    def rx_loop(self):
        rx_byte = self.read(1)
        incoming_byte_queue.put(rx_byte)

    def check_baud_rate(self, requested_baud_rate):
        """ Check that the baud rate requested is not already set. """
        if self.baudrate is not requested_baud_rate:
            return requested_baud_rate

    def send(self, data_to_send):
        """ Send data over the COM Port. """
        try:
            self.write(data_to_send)
        except serial.serialutil.SerialTimeoutException as err:
            print(repr(err))
            print("ERROR: Write Has Timed Out")
            callback_exception_handler("ERROR: Write Has Timed Out")
        except serial.serialutil.PortNotOpenError as err:
            print(repr(err))
            print("ERROR: Port " + config.COM_PORT + " Not Open")
            callback_exception_handler("ERROR: Port" + config.COM_PORT + " Not Open")
        except serial.serialutil.SerialException as err:
            print(repr(err))
            print("ERROR: The handle is invalid")
            callback_exception_handler("ERROR: The handle is invalid")


class StateMachineState(Enum):
    """ DataType class for each possible data type. """
    PENDING_FRAME = 1
    GATHERING_HEADER = 2
    READING_DATA = 3


class StateMachine(threading.Thread):
    """ StateMachine Class for the RX_Listener running on a separate Thread. """

    def __init__(self):
        """ Initialise Thread, buffer and checking variables. """
        super().__init__()
        self.frame_buffer = bytearray()
        self.delimiter_received = False
        self.test_listen = False
        self.daemon = True
        self.state = StateMachineState.PENDING_FRAME.value
        self.gathered_header = bytearray()
        self.header_count = 0
        self.data_length_count = 0
        self.data_length_bytes = bytearray()
        self.data_length = 0
        self.got_data_length = False
        self.data_count = 0
        self.data_bytes = bytearray()

    def run(self):
        """ Overloads the Thread's "run" function,
        reads directly if Test Interface is used,
        otherwise engages StateMachine.
        """
        while True:
            if self.test_listen is True:
                self.direct_read()
            else:
                self.run_state_machine()

    def run_state_machine(self):
        rx_byte = incoming_byte_queue.get()

        if self.state == StateMachineState.PENDING_FRAME.value:
            self.pending_frame(rx_byte)
        elif self.state == StateMachineState.GATHERING_HEADER.value:
            self.gathering_header(rx_byte)
        elif self.state == StateMachineState.READING_DATA.value:
            self.reading_data(rx_byte)
        else:
            self.state = StateMachineState.PENDING_FRAME.value

    def pending_frame(self, rx_byte):
        """ PENDING_FRAME State, checks for start of frame...
        (delimiter character followed by non delimiter character).
        """
        try:
            # Clear the received data buffer if it's 2 bytes
            if len(self.frame_buffer) == 2:
                self.frame_buffer.clear()
        except TypeError as err:
            print("ERROR: ", err)
            print("FIRST PASS")

        # Add byte to the frame buffer
        self.frame_buffer += rx_byte
        # Check if we have received a 0x55 followed by a non-0x55
        if (PROTOCOL_DELIMITER == self.frame_buffer[0]) and (rx_byte[0] != PROTOCOL_DELIMITER):
            # This is the start of a new frame!
            # Switch state to GATHERING_DATA
            self.state = StateMachineState.GATHERING_HEADER.value
            self.header_count = 0
        else:
            # Reenter PENDING_FRAME if start of frame not detected
            pass

    def gathering_header(self, rx_byte):
        """ GATHERING_HEADER State, reads the rest of the header. """
        # Create header bitfield buffer
        header_size = 3
        # Read a byte into Header Buffer
        self.gathered_header += rx_byte
        # Scan byte and previous byte for start of frame, pop off any double delimiter values
        self.gathered_header, self.header_count = self.delimiter_scan_and_remove(self.gathered_header,
                                                                                 self.header_count)
        # If we've read out enough bytes of the header
        if self.header_count == header_size:
            # Append gathered header onto buffer
            self.frame_buffer.extend(self.gathered_header)
            self.gathered_header.clear()
            # Check if Data Type is within range
            if int(self.frame_buffer[4]) in range(MAX_DATA_TYPES):
                # Data Type within range, switch to READING_DATA state
                self.state = StateMachineState.READING_DATA.value
            else:
                # Data Type out of range, discard message and return to PENDING_FRAME
                self.state = StateMachineState.PENDING_FRAME.value
                self.frame_buffer.clear()

    def reading_data(self, rx_byte):
        """ READING_DATA State, gathers the data length field and reads the rest of the frame,
        then if frame is valid place onto queue to be processed by the packet handler Thread.
        """
        # Create data length bitfield buffer
        data_length_size = 4

        # Iterate over Data Length bytes
        if self.data_length_count < data_length_size:
            # Read a byte into Data Length Buffer
            self.data_length_bytes += rx_byte
            # Scan byte and previous byte for start of frame, pop off any double delimiter values
            self.data_length_bytes, self.data_length_count = self.delimiter_scan_and_remove(self.data_length_bytes,
                                                                                            self.data_length_count)
        else:
            if self.got_data_length is False:
                # unpacks data_length_bytes into 32 bit unsigned integer
                try:
                    self.data_length = struct.unpack("!L", self.data_length_bytes)[0]
                except struct.error as err:
                    print(repr(err))
                    print("ERROR: Data Length is not 4 bytes")
                    callback_exception_handler("ERROR: Data Length is not 4 bytes")
                self.got_data_length = True

            # Read a byte into Data Buffer
            self.data_bytes += rx_byte
            # Scan byte and previous byte for start of frame, pop off any double delimiter values
            self.data_bytes, self.data_count, self.data_length = self.delimiter_scan_and_remove(self.data_bytes,
                                                                                                self.data_count,
                                                                                                True,
                                                                                                self.data_length)
            # If we have read out enough data bytes
            if self.data_count == self.data_length:
                invalid_frame = False
                data_type = self.frame_buffer[4]
                # Check the data type against all known data types
                if not any(x.value == data_type for x in DataType):
                    invalid_frame = True
                    callback_exception_handler("ERROR: Frame Data Type Field does not match actual type.")

                # Get the data type name to use with comparing against the right data length
                data_type_key = DataType(data_type).name

                # Check the actual data length against the expected length for the data type
                if self.data_length != DataTypeSize[data_type_key].value:
                    invalid_frame = True
                    callback_exception_handler("ERROR: Frame Data Length Field does not match actual length.")

                if invalid_frame is False:
                    # Append data length and data fields onto frame buffer
                    self.frame_buffer.extend(self.data_length_bytes + self.data_bytes)
                    # Add Frame onto queue to be processed by packet handler Thread
                    frame_queue.put(self.frame_buffer)
                    # Block until packet is processed in handler Thread
                    frame_queue.join()

                # Frame has been fully processed,
                # Reset all member variables so that the state machine can process the next frame
                self.header_count = 0
                self.gathered_header.clear()
                self.data_length = 0
                self.data_length_bytes.clear()
                self.data_length_count = 0
                self.data_length = 0
                self.data_bytes.clear()
                self.data_count = 0
                self.got_data_length = False
                self.delimiter_received = False

                # Set state to PENDING_FRAME
                self.state = StateMachineState.PENDING_FRAME.value
                # Clear the frame buffer
                self.frame_buffer.clear()

    def direct_read(self, com):
        """ DIRECT_READ State, entered if Test Interface is used to bypass State Machine """
        # Block until there is a byte to read
        rx_byte = self.read_byte(com)
        # Put byte onto queue
        direct_read_queue.put(rx_byte)

    @staticmethod
    def read_byte(com):
        """ Read and return a byte from the COM Port """
        rx_byte = com.read(1)
        return rx_byte

    def delimiter_scan_and_remove(self, buffer, index, data_field=False, data_length_decrement=0):
        """ Iterate through buffer, pop off a delimiter where there are 2 consecutive delimiter values,
        enter GATHERING_HEADER State if start of frame detected.
        """
        # If this byte is a delimiter
        if PROTOCOL_DELIMITER is buffer[index]:
            # and we haven't received a prior delimiter
            if self.delimiter_received is False:
                # Record that this byte is a delimiter
                self.delimiter_received = True
            # and we've received a prior valid delimiter
            else:
                # Discard the byte
                buffer.pop(index)
                # Rewind indexer to maintain stepping
                index -= 1
                if data_field is True:
                    # Add to data_length decrementer HERE to then take off data_length after entire read
                    data_length_decrement -= 1
                # Set state to wait for next delimiter
                self.delimiter_received = False
        # If this byte is not a delimiter
        else:
            # and we have received a prior delimiter that makes this an invalid sequence
            if self.delimiter_received is True:
                # This is the start of a new frame!
                # Set the frame buffer to this new frame
                self.frame_buffer = buffer
                # Reset received delimiter variable
                self.delimiter_received = False
                # Enter GATHERING_HEADER state
                self.state = StateMachineState.GATHERING_HEADER.value
                self.header_count = 0
                return buffer, 0
        # Increment the index
        index += 1
        if data_length_decrement == 0:
            return buffer, index
        else:
            return buffer, index, data_length_decrement


def comms_init(port, baud_rate):
    """ Initialise CommsHandler class instance , set COM Port and baud rate, start rx_listener Thread. """
    global comms_handler
    if comms_handler is not CommsHandler:
        comms_handler = CommsHandler(port, baud_rate)
        comms_handler.rx_state_machine.start()

        if RaspberryPi is True:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(DIO0_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(DIO0_GPIO, GPIO.FALLING,
                                  callback=comms_handler.radio.rx_interrupt, bouncetime=100)

        signal.signal(signal.SIGINT, signal_handler)


def comms_send(data):
    """ Send data over the COM Port"""
    global comms_handler
    if config.COMMS == "RF69" and RaspberryPi is True:
        comms_handler.radio.send(data)
    elif config.COMMS == "SERIAL":
        comms_handler.serial.send(data)


def change_baud_rate(requested_baud_rate):
    """ Change baud rate to requested rate """
    global comms_handler
    comms_handler.serial.baudrate = comms_handler.comms.check_baud_rate(requested_baud_rate)


def flush_com_port():
    global comms_handler
    comms_handler.serial.reset_output_buffer()


def change_com_port(port):
    global comms_handler
    comms_handler.serial.close()
    comms_handler.serial.port = port
    config.COM_PORT = port
    try:
        comms_handler.serial.open()
    except serial.serialutil.SerialException as err:
        print(repr(err))
