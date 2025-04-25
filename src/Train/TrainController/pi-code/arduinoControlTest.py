import serial.tools.list_ports
from time import sleep

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
portsList = []

serialInst.baudrate = 9600
serialInst.port = '/dev/ttyACM0'
serialInst.open()

serialInst.write("A\n".encode('utf-8'))

sleep(1)

serialInst.write("A\n".encode('utf-8'))

sleep(1)


serialInst.write("A\n".encode('utf-8'))

sleep(1)

serialInst.write("A\n".encode('utf-8'))

sleep(1)


serialInst.write("A\n".encode('utf-8'))

sleep(1)
serialInst.write("A\n".encode('utf-8'))

sleep(1)
serialInst.write("A\n".encode('utf-8'))

sleep(1)






serialInst.close()
