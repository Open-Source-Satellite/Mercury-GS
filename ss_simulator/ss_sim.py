"""
/***********************************************************************************
 *  @ss_sim.py
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
 *  Created on: 14-10-2021
 *  Script to simulate space station for Mercury GS                      
 *  @author: Kevin Guyll                     
 ***********************************************************************************/
"""

# doesn't recognise when a packet is too long
# extra bytes will be seen as junk
# modified so that responses correctly encode \x55

import serial
import struct, random, math
from time import sleep

#port = "COM19"
port = "COM20"

# timeout in 1/10 seconds (roughly)
TIMEOUT = 10

# possible states
WAITX55 = 0
RESBYTES = 1
DATATYPE = 2
DATALENGTH = 3
DATAFIELD = 4
COMPLETE = 5

X55_NONE = 0
X55_GOT1 = 1
X55_GOT2 = 2 

ser = serial.Serial(port, 9600, timeout=0)

def get_packet():
    state = WAITX55
    x55status = X55_NONE
    # reserved bytes count (expect 3)
    rbcount = 0
    # data length bytes count (expect 4)
    dlcount = 0
    # used to store datatype
    datatype = 0
    # length specified in data length bytes
    datalength = 0
    # bytes received in data field
    datarecvd = 0
    datafield = b''
    # used for timeout
    timecount = 0
    
    while state != COMPLETE:
      nextbyte = ser.read(1)
      if nextbyte:
        # we have received a character so reset the timeout count
        timecount = 0
        if state == DATAFIELD:
          datarecvd += 1
        if x55status:
          if nextbyte != b'\x55':
            if state:
              # Not waiting for x55 so must have invalid packet
              print('\nInvalid packet length')
            #print('\nStart of new frame')
            #print('Reserved Bytes:', end=' ')
            state = RESBYTES
            x55status = X55_NONE
            rbcount = 0
            dlcount = 0
            datarecvd = 0
            datatype = 0
            datalength = 0
            datafield = b''
          else:
            x55status = X55_GOT2
        if nextbyte == b'\x55' and x55status != X55_GOT2:
          #print('got x55', end=' ')
          x55status = X55_GOT1
        else:
          x55status = X55_NONE
          if state == RESBYTES:
            rbcount += 1
            #print(rbcount,nextbyte, end='  ')
            if rbcount == 3:
              state = DATATYPE
          elif state == DATATYPE:
            #print('\nData Type:',nextbyte)
            datatype = int.from_bytes(nextbyte, "big")
            #print(' datatype=',datatype)
            state = DATALENGTH
            #print('Data Length:', end=' ')
          elif state == DATALENGTH:
            dlcount += 1
            #print(dlcount,nextbyte, end=' ')
            datalength = (datalength * 256) + int.from_bytes(nextbyte, "big")		
            if dlcount == 4:
              state = DATAFIELD
              #print('\n datalength=', datalength)
              #print('Data:', end=' ')
          elif state == DATAFIELD:
            #print(nextbyte, end=' ')
            datafield += nextbyte
            if datarecvd == datalength:
              #print('\n Data field=', datafield)
              #state = WAITX55
              state = COMPLETE
          else: print('Junk received:', nextbyte)
      else:
        # No character available so sleep and keep a count for timeout
        if timecount >= TIMEOUT:
          #print ('Timeout')
          state = COMPLETE
          timecount = 0
        else:
          sleep(0.1)
          timecount += 1

    return (datatype, datafield) 

incycle = 0

while True:
    # packet is a tuple
    packet = get_packet()
    datatype = packet[0]
    datafield = packet[1]
    datalength = len(datafield)

    if datatype:
        print('\n', packet)
        if datatype == 1: # telecommand
            if datalength < 4:
                print('invalid telecommand')
            else:
                telecmd = datafield[0:4]
                telecmdstr = struct.unpack('>I', telecmd)
                telecmdno = telecmdstr[0]
                if datalength != 12:
                    print('invalid telecommand length')
                    response = b'\x55\xde\xad\xbe\x02\x00\x00\x00\x05' + telecmd + b'\x02'
                elif telecmdno == 1:
                    print('telecommand 1 - respond success')
                    response = b'\x55\xde\xad\xbe\x02\x00\x00\x00\x05\x00\x00\x00\x01\x00'
                elif telecmdno == 2:
                    print('telecommand 2 - respond failed')
                    response = b'\x55\xde\xad\xbe\x02\x00\x00\x00\x05\x00\x00\x00\x02\x01'
                elif telecmdno == 3:
                    print('telecommand 3 - respond invalid length')
                    response = b'\x55\xde\xad\xbe\x02\x00\x00\x00\x05\x00\x00\x00\x03\x02'
                elif telecmdno == 5:
                    print('telecommand 5 - respond invalid command argument')
                    response = b'\x55\xde\xad\xbe\x02\x00\x00\x00\x05\x00\x00\x00\x05\x04'
                else:
                    print('telecommand', telecmdno, 'not supported')
                    if telecmdno == 85:
                        response = b'\x55\xde\xad\xbe\x02\x00\x00\x00\x06\x00\x00\x00UU\x03'
                    else:
                        response = b'\x55\xde\xad\xbe\x02\x00\x00\x00\x05' + telecmd + b'\x03'
                ser.write(response)
        elif datatype == 4: # telemetry
            print('telemetry request')
            if datalength < 4:
                print('invalid telemetry channel length')
            else:
                telechan = datafield[0:4]
                telechanstr = struct.unpack('>I', telechan)
                telechanno = telechanstr[0]
                print('telechan=', telechan)
                if datalength != 4:
                    print('invalid telemetry length')
                    response = b'\x55\xde\xad\xbe\x07\x00\x00\x00\x05' + telechan + b'\x01'
                    
                # channels 1-4, 12 and 85 responses taken from test_frames files
                elif telechanno == 1:
                    response = b'\x55\xde\xad\xbe\x03\x00\x00\x00\x0c\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01'
                elif telechanno == 2:
                    response = b'\x55\xde\xad\xbe\x03\x00\x00\x00\x0c\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x02'
                elif telechanno == 3:
                    response = b'\x55\xde\xad\xbe\x03\x00\x00\x00\x0c\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x03'
                elif telechanno == 4:
                    print('telemetry channel 4 - respond invalid data length')
                    response = b'\x55\xde\xad\xbe\x07\x00\x00\x00\x05\x00\x00\x00\x04\x01'
                elif telechanno == 12:
                    response = b'\x55\xde\xad\xbe\x03\x00\x00\x00\x0c\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x00\xff'
                elif telechanno == 85:
                    response = b'\x55\xde\xad\xbe\x03\x00\x00\x00\x0f\x00\x00\x00\x55\x55\x00\x00\x00\x00\x55\x55\x55\x55\x00\xfe'
                    
                # channels 20 to 39 respond with a random number
                elif telechanno > 19 and telechanno < 40:
                    teledata = random.randint(0,255)
                    teledatab = bytes(chr(teledata),'latin-1')
                    if teledata == 85:  # case of \x55
                        response = b'\x55\xde\xad\xbe\x03\x00\x00\x00\x0d' + telechan + b'\x00\x00\x00\x00\x00\x00\x00UU'               
                    else:
                        response = b'\x55\xde\xad\xbe\x03\x00\x00\x00\x0c' + telechan + b'\x00\x00\x00\x00\x00\x00\x00' + teledatab               
                    
                # other channels respond channel not supported
                else:
                    response = b'\x55\xde\xad\xbe\x07\x00\x00\x00\x05' + telechan + b'\x00'
                    
                print('telemetry channel', telechanno, response)
                ser.write(response)
                #sleep(5)
                #ser.write(response)
        else:
            print('other data type')

    # Generate telemetry data for channel 42
    t = int(random.randint(60, 80) * (1 + math.sin(incycle)))
    x = bytes(chr(t),'latin-1')

    if t == 85: # case of \x55
        response = b'\x55\xde\xad\xbe\x03\x00\x00\x00\x0d\x00\x00\x00\x2a\x00\x00\x00\x00\x00\x00\x00UU'
    else:
        response = b'\x55\xde\xad\xbe\x03\x00\x00\x00\x0c\x00\x00\x00\x2a\x00\x00\x00\x00\x00\x00\x00' + x
    incycle += 0.01
    if incycle >= 2 * math.pi:
        incycle = 0
    
    # uncomment next line to receive telemetry on channel 42
    ser.write(response)
    
ser.close()
