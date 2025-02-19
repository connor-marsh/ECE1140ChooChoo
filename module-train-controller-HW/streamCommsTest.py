# run.py
from paramiko import SSHClient
import time
from threading import Thread
import json
from copy import deepcopy

ssh = SSHClient()
ssh.load_system_host_keys()

ssh.connect("10.6.19.80", username="connor-marsh", password="ece1140")
print("SSH Connected")

print('started...')
stdin, stdout, stderr = ssh.exec_command('python pi_train_controller.py ssssh', get_pty=True)


# Format for sending data, its a 1d array that just lists out all the important data
# [actualSpeed, position, ebrake state, temperature, failure 1, failure 2, failure 3]
# Format for receiving data, its a 1d array that just lists out all the important data
# [commanded power, position, ebrake state, temperature, failure 1, failure 2, failure 3]


sendData = {}

def ssh_handler():
    global sendData
    prevData = {}
    while True:
        if not sendData==prevData:
            print("Sending over SSH")
            stdin.write(json.dumps(sendData)+'\n')
            stdout.readline()
            prevData = deepcopy(sendData)

            print("Read in: " + stdout.readline().rstrip())
            


def input_handler():
    global sendData
    tempDataFormat = ["actual_speed", "commanded_speed", "authority", "position", "ebrake_state", "temperature"]
    while True:
        inputData = input("Input smth")
        if inputData=="\q":
            return
        dataList=inputData.split(' ')
        for i in range(len(dataList)):
            sendData[tempDataFormat[i]] = float(dataList[i])

ssh_thread=Thread(target=ssh_handler)
ssh_thread.start()
input_thread=Thread(target=input_handler)
input_thread.start()
input_thread.join()
ssh_thread.join()
print("Ended threads")