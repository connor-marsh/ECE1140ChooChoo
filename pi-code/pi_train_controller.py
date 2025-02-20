import time
import sys
import fileinput
from threading import Thread
from gpiozero import LED, Button
import json
from copy import deepcopy
from luma.core.render import canvas
from luma.oled.device import ssd1306
from luma.core.interface.serial import i2c

pins = {
    "manualSwitch":Button(4, pull_up=True),
    "headlightsSignal":LED(17),
    "headlightsSwitch":Button(27, pull_up=True),
    "lightsSignal":LED(22),
    "lightsSwitch":Button(10, pull_up=True),
    "leftDoorsSignal":LED(9),
    "leftDoorsSwitch":Button(11, pull_up=True),
    "rightDoorsSignal":LED(0),
    "rightDoorsSwitch":Button(5, pull_up=True),
    "AC":LED(6),
    "heat":LED(13),
    "brakes":LED(19),
    "brakeFailure":LED(26),
    "engineFailure":LED(21),
    "signalFailure":LED(20),
    "ebrakeSignal":LED(16),
    "ebrakeButton":Button(12, pull_up=True),
}

def ebrakeHandler():
    global ebrake
    ebrake = not ebrake
pins["ebrakeButton"].when_pressed = ebrakeHandler

dt = 0.1
speedLimit = 60.0
targetSpeed = 0.0
intError = 0.0
kP=0.5
kI=0.1
driverInputSpeed = 0.0
driverInputTemperature = 25.0
manualMode = False
headlights = False
lights = False
leftDoors=False
rightDoors=False
AC=False
acTimeOff = 0.0
heat=False
heatTimeOff = 0.0
tempTimeOffThreshold = 40
brakes=False
brakeFailure=False
engineFailure=False
signalFailure=False
ebrake=False
timeElapsed=0.0

serial1 = i2c(port=1, address=0x3c)
device1 = ssd1306(serial1)

serial2 = i2c(port=1, address=0x3d)
device2 = ssd1306(serial2)

receiveDataFormat = ["actual_speed", "commanded_speed", "authority", "position", "ebrake_state", "temperature", "brake_failure", "engine_failure", "signal_failure"]
sendDataFormat = ["commanded_power"]
receiveData = {}
sendData = {}
for word in receiveDataFormat:
    receiveData[word]=0.0
for word in sendDataFormat:
    sendData[word]=0.0
    
def sshStreamHandler():
    global receiveData, sendData
    for line in sys.stdin:
        receiveData = json.loads(line.rstrip())
        processReceivedData()
        print(json.dumps(sendData))

def ioHandler():
    global sendData, manualMode, headlights, lights, rightDoors, leftDoors, AC, heat, brakes, brakeFailure, engineFailure, signalFailure, ebrake
    prevDataLines1 = []
    prevDataLines2 = []
    while True:
        
        manualMode = pins["manualSwitch"].is_pressed
        headlights = pins["headlightsSwitch"].is_pressed if manualMode else headlights
        lights = pins["lightsSwitch"].is_pressed if manualMode else lights
        rightDoors = pins["rightDoorsSwitch"].is_pressed if manualMode and receiveData["actual_speed"]<0.5 else rightDoors
        leftDoors = pins["leftDoorsSwitch"].is_pressed if manualMode and receiveData["actual_speed"]<0.5 else leftDoors
        
        pins["headlightsSignal"].on() if headlights else pins["headlightsSignal"].off()
        pins["lightsSignal"].on() if lights else pins["lightsSignal"].off()
        pins["rightDoorsSignal"].on() if rightDoors else pins["rightDoorsSignal"].off()
        pins["leftDoorsSignal"].on() if leftDoors else pins["leftDoorsSignal"].off()
        pins["AC"].on() if AC else pins["AC"].off()
        pins["heat"].on() if heat else pins["heat"].off()
        pins["brakes"].on() if brakes else pins["brakes"].off()
        pins["brakeFailure"].on() if brakeFailure else pins["brakeFailure"].off()
        pins["engineFailure"].on() if engineFailure else pins["engineFailure"].off()
        pins["signalFailure"].on() if signalFailure else pins["signalFailure"].off()
        pins["ebrakeSignal"].on() if ebrake else pins["ebrakeSignal"].off()
        
        dataLines1 = [receiveData["actual_speed"], speedLimit, targetSpeed, driverInputSpeed, receiveData["authority"], sendData["commanded_power"]]
        dataLines2 = [dt, "e.g.", receiveData["temperature"], driverInputTemperature, kP, kI]
        if not prevDataLines1 == dataLines1:
            with canvas(device1, dither=True) as draw:
                textLines = ["Real Speed(mph): ", "Speed Limit(mph): ", "Target Speed(mph): ", "Input Speed(mph): ", "Authority(ft): ", "Power Out(W): "]
                for i in range(len(textLines)):
                    draw.text((2,i*10), textLines[i] + str(dataLines1[i]))
            prevDataLines1 = dataLines1
        if not prevDataLines2 == dataLines2:
            with canvas(device2, dither=True) as draw:
                textLines = ["Time: ", "Next Station: ", "Actual Temp: ", "Desired Temp: ", "K_p: ", "K_i: "]
                for i in range(len(textLines)):
                    draw.text((2,i*10), textLines[i] + str(dataLines2[i]))
            prevDataLines2 = dataLines2
        time.sleep(0.001)

def printingHandler():
    global receiveData, sendData
    prevData = {}
    while True:
        if receiveData=="\q":
            return
        if not receiveData==prevData:
            processReceivedData()
            print("Inputted: " + str(sendData))
            prevData = deepcopy(receiveData)
            

def manualInputHandler():
    global receiveData
    
    print("Input smth")
    while True:
        inputData = input()
        if inputData=="\q":
            return
        dataList=inputData.split( )
        for i in range(len(dataList)):
            receiveData[receiveDataFormat[i]] = float(dataList[i])
            
def processReceivedData():
    global sendData, intError, targetSpeed, brakes, ebrake, brakeFailure, engineFailure, signalFailure
    targetSpeed = driverInputSpeed if manualMode else receiveData["commanded_speed"]
    targetSpeed = speedLimit if targetSpeed > speedLimit else targetSpeed
    error = targetSpeed - receiveData["actual_speed"]
    intError += error*dt
    power = kP*error + kI*intError
    power = 0 if power < 0 else (120000 if power > 120000 else power)
    sendData["commanded_power"] = power
    
    brakes = error < 0
    
    # convert sent data from floats to bools
    ebrake = receiveData["ebrake_state"] == 1.0
    brakeFailure = receiveData["brake_failure"] == 1.0
    engineFailure = receiveData["engine_failure"] == 1.0
    signalFailure = receiveData["signal_failure"] == 1.0
    
    

if len(sys.argv)>1:
    if sys.argv[1]=="ssh":
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

