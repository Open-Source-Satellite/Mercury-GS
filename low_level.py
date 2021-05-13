###################################################################################
# @file low_level.py
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
#  Mercury GS Low Level Driver
#  @author: Jamie Bayley (jbayley@kispe.co.uk)
###################################################################################

import serial
import config
import threading

ser = serial.Serial()


def register_callback(unpacketize_function_ptr):
    global callback_unpacketize
    callback_unpacketize = unpacketize_function_ptr


def rx_listener(com):
    while True:
        if com.in_waiting != 0:
            rx_data = com.read(com.in_waiting).decode()
            receive(rx_data)


rx_listener_thread = threading.Thread(target=rx_listener, args=(ser,))


def send(data_to_send):
    change_baud_rate(config.BAUD_RATE)
    print(ser.name)
    print(ser.baudrate)
    ser.write(bytearray(data_to_send, "utf8"))


def receive(received_data):
    callback_unpacketize(received_data)


def init():
    change_baud_rate(config.BAUD_RATE)
    ser.port = 'COM19'
    ser.bytesize = 8
    # ser.write_timeout = 5

    if ser.is_open:
        ser.close()

    if not ser.is_open:
        ser.open()

    print(ser.is_open)
    if not rx_listener_thread.is_alive():
        rx_listener_thread.start()


def change_baud_rate(requested_baud_rate):
    if ser.baudrate is not requested_baud_rate:
        ser.baudrate = requested_baud_rate
