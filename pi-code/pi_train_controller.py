import time
import sys
import fileinput
from threading import Thread
from gpiozero import LED
import json
from copy import deepcopy
from luma.core.render import canvas
from luma.oled.device import ssd1306
from luma.core.interface.serial import i2c

led=LED(23)
speedLimit = 60.0
intError = 0.0
kP=0.5
kI=0.1
manualMode = False
driverSpeed = 0.0

serial1 = i2c(port=1, address=0x3c)
device1 = ssd1306(serial1)

serial2 = i2c(port=1, address=0x3d)
device2 = ssd1306(serial2)




receiveData = {}
sendData = {}
def sshStreamHandler():
    global receiveData, sendData, intError
    #stream = fileinput.input()
    for line in sys.stdin:
        receiveData = json.loads(line.rstrip())
        dt = 0.1
        targetSpeed = driverSpeed if manualMode else receiveData["commanded_speed"]
        targetSpeed = speedLimit if targetSpeed > speedLimit else targetSpeed
        error = targetSpeed - receiveData["actual_speed"]
        intError += error*dt
        power = kP*error + kI*intError
        sendData = {}
        sendData["commanded_power"] = power
        print(json.dumps(sendData))

def ioHandler():
    global receiveData, sendData
    while True:
        if not "actual_speed" and "commanded_speed" in receiveData or not "commanded_power" in sendData:
            continue
        
        if receiveData["actual_speed"]>speedLimit:
            led.on()
        else:
            led.off()
            
        with canvas(device1, dither=True) as draw:
            #fill, outline = "black", "white"
            #textLines = ["Actual Speed(mph): ", "Speed Limit(mph): ", "Target Speed(mph): ", "Input Speed(mph): ", "Authority(ft): ", "Power Out(W): "]
            textLines = ["GOOBER Power(W): "]
            dataLines = [33, 50, 40, 20, 4000, 4000.12]
            dataLines[0] = sendData["commanded_power"]
            for i in range(len(textLines)):
                draw.text((2,i*10), textLines[i] + str(dataLines[i]))
        with canvas(device2, dither=True) as draw:
            #fill, outline = "black", "white"
            #textLines = ["Actual Speed(mph): ", "Speed Limit(mph): ", "Target Speed(mph): ", "Input Speed(mph): ", "Authority(ft): ", "Power Out(W): "]
            textLines = ["Power(W): "]
            dataLines = [33, 50, 40, 20, 4000, 4000.12]
            dataLines[0] = sendData["commanded_power"]
            for i in range(len(textLines)):
                draw.text((2,i*10), textLines[i] + str(dataLines[i]))
        time.sleep(0.001)

def printingHandler():
    global receiveData, sendData, intError
    prevData = {}
    while True:
        if receiveData=="\q":
            return
        if not receiveData==prevData:
            dt = 0.1
            targetSpeed = driverSpeed if manualMode else receiveData["commanded_speed"]
            targetSpeed = speedLimit if targetSpeed > speedLimit else targetSpeed
            error = targetSpeed - receiveData["actual_speed"]
            intError += error*dt
            power = kP*error + kI*intError
            sendData["commanded_power"] = power
            print("Inputted: " + str(sendData))
            prevData = deepcopy(receiveData)
            

def manualInputHandler():
    global receiveData
    tempDataFormat = ["actual_speed", "commanded_speed", "authority", "position", "ebrake_state", "temperature"]
    print("Input smth")
    while True:
        inputData = input()
        if inputData=="\q":
            return
        dataList=inputData.split( )
        for i in range(len(dataList)):
            receiveData[tempDataFormat[i]] = int(dataList[i])

if len(sys.argv)>1:
    if sys.argv[1]=="ssssh":
        inputThread=Thread(target=sshStreamHandler)
    else:
        inputThread=Thread(target=manualInputHandler)
        outputThread = Thread(target=printingHandler)
        outputThread.start()
else:
    inputThread=Thread(target=manualInputHandler)
    outputThread = Thread(target=printingHandler)
    outputThread.start()

inputThread.start()
ioThread = Thread(target=ioHandler)
ioThread.start()

inputThread.join()
ioThread.join()
print("Terminating main")

