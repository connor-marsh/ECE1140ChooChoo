from paramiko import SSHClient
from scp import SCPClient
import numpy as np
import time
from threading import Thread

numDataPoints = 7
inputData="0"
ssh = SSHClient()
ssh.load_system_host_keys()
print("Connecting to SSH")
ssh.connect("10.6.19.80", username="connor-marsh", password="ece1140")
print("SSH Connected")

# IMPORTANT NOTE:
# Format for numpy data, its a 1d array that just lists out all the important data
# [actualSpeed, position, ebrake state, temperature, failure 1, failure 2, failure 3]
# the ones that are booleans will just be a 1 or a 0, even though the dtype=float

# SCPCLient takes a paramiko transport as an argument
scp = SCPClient(ssh.get_transport())
def display_thread():
    global inputData
    prevData =np.zeros(numDataPoints) 
    while True:
        if inputData=="\q":
            return
        data = np.zeros(numDataPoints)
        inputDataList = inputData.split(' ')
        for i in range(len(inputDataList)):
            data[i] = int(inputDataList[i])
        if not np.all(data==prevData):
            # print("Sending over SCP")
            # np.save("pcToPi.npy", data)
            # scp.put('pcToPi.npy', remote_path='/home/connor-marsh')
            # prevData = data

            # print("receiving data over SCP")
            # scp.get('piToPc.npy')
            # bothWays = np.load("piToPc.npy")
            # print(bothWays)

            # silly backand forth timing checker
            start_time = time.time_ns()
            for i in range(10):
                data[0] += 1
                np.save("pcToPi.npy", data)
                scp.put('pcToPi.npy', remote_path='/home/connor-marsh')
                prevData = data

                # print("receiving data over SCP: " + str(i))
                scp.get('piToPc.npy')
                data = np.load("piToPc.npy")
                # print(data)
            print("Time: " + str((time.time_ns()-start_time)/1000000))
            return

def input_thread():
    global inputData
    while True:
        inputData = input("Input smth")
        if inputData=="\q":
            return 

thread1=Thread(target=display_thread)
thread1.start()
thread2=Thread(target=input_thread)
thread2.start()
thread2.join()
thread1.join()
print("Ended threads")


scp.close()
