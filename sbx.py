import serial
from time import sleep

port = "/tmp/master"

serialPort = serial.Serial(port, 115200, timeout=0)
x = serialPort.write(b'hello')

while True:
    data = serialPort.read(9999)
    if len(data) > 0:
        print("Got : ", data)
    else:
        sleep(0.5)
        print("not blocked")

serialPort.close()