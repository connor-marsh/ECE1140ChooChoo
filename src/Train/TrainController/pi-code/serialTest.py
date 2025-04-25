import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
portsList = []

for port in ports:
    portsList.append(str(port))
    print(str(port))


serialInst.baudrate =  115200
