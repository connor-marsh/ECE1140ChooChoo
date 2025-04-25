import serial
from time import sleep


baudrate = 9600
port = '/dev/ttyACM0'
ser = serial.Serial(port, baudrate)

sleep(2)
t=0
# This code relies on pi and arduino running at same update speed
# So u need to flush the input when you start reading to make sure they are aligned
ser.flushInput()
while t<10:
    print(ser.readline().decode('utf-8'))
    sleep(0.1)
    t+=0.1
