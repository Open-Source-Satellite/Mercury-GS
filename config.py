###################################################################################
# @file config.py
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
#  Mercury GS Global Variables
#  @author: Jamie Bayley (jbayley@kispe.co.uk)
###################################################################################
import platform
try:
    import RPi.GPIO as GPIO
    RaspberryPi = True
except(ImportError, RuntimeError):
    RaspberryPi = False

# Initialise Global Variables
OS = platform.system()
BAUD_RATE = 9600
COM_PORT = "COM1"
COMMS = "RF69"
TC_TLM_RATE = 1
TIMEOUT = float(1000) / 1000


def config_register_callback(exception_handler_function_ptr):
    """ Registers the callbacks for this module to pass data back to previous modules. """
    global callback_exception_handler
    # Register exception handler callback
    callback_exception_handler = exception_handler_function_ptr


def change_timeout(timeout):
    """ Change the global TIMEOUT value as a float. """
    global TIMEOUT
    try:
        TIMEOUT = float(timeout) / 1000
    except ValueError as err:
        print("ERROR: ", err)
        print("INFO: Invalid Timeout Value")
        callback_exception_handler("ERROR: Invalid Timeout Value")


# Function Pointers
global ptr_unpacketise
global ptr_telemetry_update
global ptr_telecommand_response_update
