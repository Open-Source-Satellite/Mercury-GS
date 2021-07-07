"""
/***********************************************************************************
 *  @simplereceiver.py
 ***********************************************************************************
 *   _  _____ ____  ____  _____ 
 *  | |/ /_ _/ ___||  _ \| ____|
 *  | ' / | |\___ \| |_) |  _|  
 *  | . \ | | ___) |  __/| |___ 
 *  |_|\_\___|____/|_|   |_____|
 *
 ***********************************************************************************
 *  Copyright (c) 2021 KISPE Space Systems Ltd.
 *  
 *  https://www.kispe.co.uk/projectlicenses/RA2001001003
 ***********************************************************************************
 *  Created on: 07-07-2021                      
 *  Modified version for Python3     
 *  Original author: Eli Bendersky
 *  https://eli.thegreenplace.net/2009/07/30/setting-up-python-to-work-with-the-serial-port/
 *  Modified by: Kevin Guyll                     
 ***********************************************************************************/
"""

# Simple script to receive and print output from Mercury GS

import serial
from time import sleep

#port = "COM19"
port = "COM20"
ser = serial.Serial(port, 9600, timeout=0)

while True:
    data = ser.read(9999)
    if len(data) > 0:
        print('Got:', data)
    else:
		# code modified so that it only sleeps if there is no data
        sleep(0.5)
        # print('not blocked')

ser.close()
