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
import serial

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
    "brakesSwitch":Button(13, pull_up=True),
    "heat":LED(6),
    "brakes":LED(19),
    "brakeFailure":LED(26),
    "engineFailure":LED(21),
    "signalFailure":LED(20),
    "ebrakeSignal":LED(16),
    "ebrakeButton":Button(12, pull_up=True),
}

def ebrakeHandler():
    global ebrake, passengerEBrakeOverride
    ebrake = not ebrake
    passengerEBrakeOverride = True
pins["ebrakeButton"].when_pressed = ebrakeHandler

speedLimit = 60.0
targetSpeed = 0.0
intError = 0.0
kP=20000
kI=75
driverInputSpeed = 20
driverInputTemperature = 25.0
manualMode = False
headlights = False
lights = False
leftDoors=False
rightDoors=False
AC=False
heat=False
brakes=False
brakeFailure=False
engineFailure=False
signalFailure=False
ebrake=False
passengerEBrakeOverride = False
annunciation = "e.g."
realTime = 7*60*60
timeString = "7:00"

serial1 = i2c(port=1, address=0x3c)
device1 = ssd1306(serial1)

serial2 = i2c(port=1, address=0x3d)
device2 = ssd1306(serial2)

receiveDataFormat = ["actual_speed", "speed_limit", "wayside_speed", "wayside_authority", "emergency_brake", "actual_temperature", "brake_failure", "engine_failure", "signal_failure", "service_brake", "left_doors", "right_doors", "headlights", "interior_lights", "air_conditioning_signal", "heating_signal", "announcements", "time_string", "time_multiplier", "dt", "kp", "ki", "commanded_power"]
sendDataFormat = ["commanded_power", "emergency_brake", "service_brake", "left_doors", "right_doors", "headlights", "interior_lights", "desired_temperature", "manual_mode"]
receiveData = {}
sendData = {}
for word in receiveDataFormat:
    receiveData[word]=0.0
for word in sendDataFormat:
    sendData[word]=0.0
    if word == "annunciation":
        sendData[word]=""
    
def sshStreamHandler():
    global receiveData, sendData
    for line in sys.stdin:
        receiveData = json.loads(line.rstrip())
        processReceivedData()
        print(json.dumps(sendData))

def ioHandler():
    global sendData, manualMode, headlights, lights, rightDoors, leftDoors, AC, heat, brakes, brakeFailure, engineFailure, signalFailure, ebrake, timeString
    prevDataLines1 = []
    prevDataLines2 = []
    while True:
        
        manualMode = pins["manualSwitch"].is_pressed
        headlights = pins["headlightsSwitch"].is_pressed if manualMode else receiveData["headlights"]
        lights = pins["lightsSwitch"].is_pressed if manualMode else receiveData["interior_lights"]
        rightDoors = pins["rightDoorsSwitch"].is_pressed if manualMode else receiveData["right_doors"]
        leftDoors = pins["leftDoorsSwitch"].is_pressed if manualMode else receiveData["left_doors"]
        rightDoors = rightDoors if receiveData["actual_speed"]<0.1 else False
        leftDoors = leftDoors if receiveData["actual_speed"]<0.1 else False
        brakes = pins["brakesSwitch"].is_pressed if manualMode else receiveData["service_brake"]
        
        pins["headlightsSignal"].on() if headlights else pins["headlightsSignal"].off()
        pins["lightsSignal"].on() if lights else pins["lightsSignal"].off()
        pins["rightDoorsSignal"].on() if rightDoors else pins["rightDoorsSignal"].off()
        pins["leftDoorsSignal"].on() if leftDoors else pins["leftDoorsSignal"].off()
        pins["brakes"].on() if brakes else pins["brakes"].off()
        pins["brakeFailure"].on() if brakeFailure else pins["brakeFailure"].off()
        pins["engineFailure"].on() if engineFailure else pins["engineFailure"].off()
        pins["signalFailure"].on() if signalFailure else pins["signalFailure"].off()
        pins["ebrakeSignal"].on() if ebrake else pins["ebrakeSignal"].off()
        
        dataLines1 = [receiveData["actual_speed"], speedLimit, targetSpeed, driverInputSpeed, receiveData["wayside_authority"], receiveData["commanded_power"]]
        dataLines2 = [timeString, annunciation, receiveData["actual_temperature"], driverInputTemperature, kP, kI]
        
        if not prevDataLines1 == dataLines1:
            with canvas(device1, dither=True) as draw:
                textLines = ["Real Speed(mph): ", "Speed Limit(mph): ", "Target Speed(mph): ", "Input Speed(mph): ", "Authority(ft): ", "Power Out(W): "]
                for i in range(len(textLines)):
                    draw.text((2,i*10), textLines[i] + str(dataLines1[i]))
            prevDataLines1 = dataLines1
        if not prevDataLines2 == dataLines2:
            with canvas(device2, dither=True) as draw:
                textLines = ["Time: ", "Stop: ", "Actual Temp: ", "Desired Temp: ", "K_p: ", "K_i: "]
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
    global sendData, intError, targetSpeed, speedLimit, brakes, ebrake, passengerEBrakeOverride, brakeFailure, engineFailure, signalFailure, AC, heat, realTime, timeString, timeSignal, kP, kI, annunciation
    speedLimit = receiveData["speed_limit"]
    targetSpeed = driverInputSpeed if manualMode else receiveData["wayside_speed"]
    targetSpeed = speedLimit*0.9 if targetSpeed > speedLimit*0.9 else targetSpeed
    error = targetSpeed - receiveData["actual_speed"]
    intError += error*receiveData["dt"]/1000*receiveData["time_multiplier"]
    intError = 0 if error < 0 else intError
    kP = receiveData["kp"]
    kI = receiveData["ki"]
    power1 = kP*error + kI*intError
    power2 = kP*error + kI*intError
    power3 = kP*error + kI*intError
    power = 0
    if power1 == power2 and power1 and power1 == power3:
        power = power1 if power1 < 120000 else 120000
        power = power if power > 0 else 0
    else:
        power = 0
    
    # convert received data from floats to bools
    if not passengerEBrakeOverride:
        ebrake = receiveData["emergency_brake"] == 1.0
    brakeFailure = receiveData["brake_failure"] == 1.0
    engineFailure = receiveData["engine_failure"] == 1.0
    signalFailure = receiveData["signal_failure"] == 1.0
    
    temperature = receiveData["actual_temperature"]
    annunciation = receiveData["announcements"]
        
    # time calc
    timeString = receiveData["time_string"]
    
    # set send data to output back to main system
    sendData["commanded_power"] = power
    sendData["service_brake"] = brakes
    sendData["emergency_brake"] = ebrake
    sendData["left_doors"] = leftDoors
    sendData["right_doors"] = rightDoors
    sendData["headlights"] = headlights
    sendData["interior_lights"] = lights
    sendData["desired_temperature"] = driverInputTemperature
    sendData["manual_mode"] = manualMode
    passengerEBrakeOverride=False
    
def arduinoHandler():
    global driverInputSpeed, driverInputTemperature
    ser = serial.Serial('/dev/ttyACM0', 9600)
    time.sleep(2)

    ser.flushInput()
    while True:
        text = ser.readline().decode('utf-8').split(' ')
        driverInputSpeed = int(text[0])
        driverInputTemperature = int(text[1])

    time.sleep(0.1)

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
arduinoThread = Thread(target=arduinoHandler)
arduinoThread.start()

inputThread.join()
ioThread.join()
arduinoThread.join()
print("Terminating main")

