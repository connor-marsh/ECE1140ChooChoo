import time
import sys
import fileinput
from threading import Thread
from gpiozero import LED
import json
from copy import deepcopy
led=LED(23)

sendData = {}
def sshStreamHandler():
    global sendData
    #stream = fileinput.input()
    for line in sys.stdin:
        sendData = json.loads(line.rstrip())
        print(json.dumps(sendData))

def ioHandler():
    global sendData
    while True:
        if sendData.get("actual_speed", 0)==1:
            led.on()
        else:
            led.off()
        time.sleep(0.001)

def printingHandler():
    global sendData
    prevData = {}
    while True:
        if sendData=="\q":
            return
        if not sendData==prevData:
            print("Inputted: " + str(sendData))
            prevData = deepcopy(sendData)

def manualInputHandler():
    global sendData
    tempDataFormat = ["actual_speed", "position", "ebrake_state", "temperature"]
    print("Input smth")
    while True:
        inputData = input()
        if inputData=="\q":
            return
        dataList=inputData.split( )
        for i in range(len(dataList)):
            sendData[tempDataFormat[i]] = int(dataList[i])

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
