"""
/***********************************************************************************
 *  @com_monitor.py
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

#import Queue
import queue
import threading
import time

import serial


class ComMonitorThread(threading.Thread):
    """ A thread for monitoring a COM port. The COM port is 
        opened when the thread is started.
    
        data_q:
            Queue for received data. Items in the queue are
            (data, timestamp) pairs, where data is a binary 
            string representing the received data, and timestamp
            is the time elapsed from the thread's start (in 
            seconds).
        
        error_q:
            Queue for error messages. In particular, if the 
            serial port fails to open for some reason, an error
            is placed into this queue.
        
        port:
            The COM port to open. Must be recognized by the 
            system.
        
        port_baud/stopbits/parity: 
            Serial communication parameters
        
        port_timeout:
            The timeout used for reading the COM port. If this
            value is low, the thread will return data in finer
            grained chunks, with more accurate timestamps, but
            it will also consume more CPU.
    """
    def __init__(   self, 
                    data_q, error_q, 
                    port_num,
                    port_baud,
                    port_stopbits=serial.STOPBITS_ONE,
                    port_parity=serial.PARITY_NONE,
                    port_timeout=0.01):
        threading.Thread.__init__(self)
        
        self.serial_port = None
        self.serial_arg = dict( port=port_num,
                                baudrate=port_baud,
                                stopbits=port_stopbits,
                                parity=port_parity,
                                timeout=port_timeout)

        self.data_q = data_q
        self.error_q = error_q
        
        self.alive = threading.Event()
        self.alive.set()
        
    def run(self):

        try:
            if self.serial_port: 
                self.serial_port.close()
            self.serial_port = serial.Serial(**self.serial_arg)
        #except serial.SerialException, e:
        except (serial.SerialException, e):
            self.error_q.put(e.message)
            return
        
        # Restart the clock
        #time.clock()
        time.perf_counter()
        
        while self.alive.isSet():
            # Reading 1 byte, followed by whatever is left in the
            # read buffer, as suggested by the developer of 
            # PySerial.
            # 
            data = self.serial_port.read(1)
            data += self.serial_port.read(self.serial_port.inWaiting())
            
            if len(data) > 0:
                #timestamp = time.clock()
                timestamp = time.perf_counter()
                self.data_q.put((data, timestamp))
            
        # clean up
        if self.serial_port:
            self.serial_port.close()

    def join(self, timeout=None):
        self.alive.clear()
        threading.Thread.join(self, timeout)

