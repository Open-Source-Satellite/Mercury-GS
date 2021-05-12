"""
/***********************************************************************************
 *  @serialutils.py
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
 *  https://github.com/eliben/code-for-blog/tree/master/2009/eblib
 *  Modified by: Kevin Guyll                     
 ***********************************************************************************/

Some serial port utilities for Windows and PySerial
"""

import re, itertools
#import _winreg as winreg
import winreg

   
def full_port_name(portname):
    """ Given a port-name (of the form COM7, 
        COM12, CNCA0, etc.) returns a full 
        name suitable for opening with the 
        Serial class.
    """
    m = re.match('^COM(\d+)$', portname)
    if m and int(m.group(1)) < 10:
        return portname    
    return '\\\\.\\' + portname    
    

def enumerate_serial_ports():
    """ Uses the Win32 registry to return an 
        iterator of serial (COM) ports 
        existing on this computer.
    """
    path = 'HARDWARE\\DEVICEMAP\\SERIALCOMM'
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
    except WindowsError:
        raise StopIteration

    for i in itertools.count():
        try:
            val = winreg.EnumValue(key, i)
            yield str(val[1])
        except EnvironmentError:
            break


#if __name__ == "__main__":
#    import serial
#    for p in enumerate_serial_ports():
#        print p, full_port_name(p)
        


