import numpy as np
import os
from time import sleep
from copy import deepcopy
prevData = np.zeros(4)
while True:
    if os.path.exists("pcToPi.npy"):
        data = np.load("pcToPi.npy")
    else:
        data = prevData
    newData = False
    if data.shape==prevData.shape:
        if not np.all(data == prevData):
            newData = True
    else:
        newData = True
    if newData:
        print("new data: " + str(data))
        prevData = data
        modData = deepcopy(data)
        modData[0] += 20
        np.save("piToPc.npy", modData)

    sleep(0.01)


