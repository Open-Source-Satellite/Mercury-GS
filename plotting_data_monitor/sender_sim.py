"""
/***********************************************************************************
 *  @sender_sim.py
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
 *  Created on: 12-05-2021                      
 *  Modified version for Python3 and PyQt5       
 *  Original author: Eli Bendersky
 *  https://github.com/eliben/code-for-blog/tree/master/2009/plotting_data_monitor
 *  Modified by: Kevin Guyll                     
 ***********************************************************************************/
"""

import serial
import random, time, math

##port = "\\\\.\\CNCB0"
port = "COM4"
ser = serial.Serial(port, 38400)

incycle = 0

while True:
    t = int(random.randint(60, 80) * (1 + math.sin(incycle)))
    ##x = ser.write(chr(t))
    print(t)
    x = ser.write(bytes(chr(t),'latin-1'))
    time.sleep(0.02)
    
    incycle += 0.01
    if incycle >= 2 * math.pi:
        incycle = 0


ser.close()

