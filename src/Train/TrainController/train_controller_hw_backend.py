"""
Author: Connor Marsh
Date: 04-02-2025
Description:

"""

# run.py
from paramiko import SSHClient
import json
from copy import deepcopy
import sys
import os

# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
# from PyQt5.QtCore import QTimer, QTime

from Train.TrainController.train_controller_backend import TrainController
from globals.settings import USING_HARDWARE


ssh = SSHClient()
ssh.load_system_host_keys()

# In order for this to work. The main PC must be connected to the raspi via ethernet
# The main PC must have its ethernet settings configured such that:
# IP = 192.168.137.1
# Subnet Mask = 255.255.255.0
# The raspi must have its wired connection settings configured such that:
# IP = 192.168.137.10
# Subnet Mask = 24
# Gateway = 192.168.137.1 (IP of the host device)

if USING_HARDWARE:
    ssh.connect("192.168.137.10", username="connor-marsh", password="ece1140")
    print("SSH Connected")

    print('Starting Raspi Program...')
    stdin, stdout, stderr = ssh.exec_command('python ~/ECE1140ChooChoo/pi-code/pi_train_controller.py ssh', get_pty=True)


# Format for sending data, its a 1d array that just lists out all the important data
sendDataFormat = ["actual_speed", "speed_limit" "wayside_speed", "wayside_authority", "emergency_brake", "kp", "ki",
                  "actual_temperature", "brake_failure", "engine_failure", "signal_failure", "dt",
                  "time_string", "time_multiplier", "service_brake", "left_doors", "right_doors", "headlights",
                  "interior_lights", "air_conditioning_signal", "heating_signal", "announcements", "commanded_power"]

# Format for receiving data, its a 1d array that just lists out all the important data
readDataFormat = ["commanded_power", "emergency_brake",
                  "service_brake", "left_doors", "right_doors", "headlights",
                  "interior_lights", "desired_temperature", "manual_mode"]
sendData = {}
readData = {}
for word in sendDataFormat:
    sendData[word]=0.0
    readData[word]=0.0
    if word == "announcements":
        sendData[word]="e.g."
        readData[word]="e.g."
for word in readDataFormat:
    readData[word]=0.0

class TrainControllerHW(TrainController):
    def __init__(self, train_integrated=True):
        super().__init__(train_integrated=train_integrated)

    def update(self):
        self.update_hardware()
        self.update_track_location()
        self.update_auxiliary()
        self.update_safety()

    def update_hardware(self):
        # Send data to and retrive data from raspi
        # Raspi does the power calculation, and has a hardware UI, and thats it
        # sendDataFormat = ["actual_speed", "wayside_speed", "wayside_authority", "emergency_brake",
        #           "actual_temperature", "brake_failure", "engine_failure", "signal_failure", "dt",
        #           "time_string", "time_multiplier", "service_brake", "left_doors", "right_doors", "headlights",
        #           "interior_lights", "air_conditioning_signal", "heating_signal", "announcements"]
        
        sendData["actual_speed"] = self.actual_speed
        sendData["speed_limit"] = self.speed_limit
        sendData["wayside_speed"] = self.wayside_speed
        sendData["wayside_authority"] = self.wayside_authority
        sendData["emergency_brake"] = self.emergency_brake
        sendData["actual_temperature"] = self.actual_temperature
        sendData["brake_failure"] = self.brake_failure
        sendData["engine_failure"] = self.engine_failure
        sendData["signal_failure"] = self.signal_failure
        sendData["service_brake"] = self.service_brake
        sendData["left_doors"] = self.left_doors
        sendData["right_doors"] = self.right_doors
        sendData["headlights"] = self.headlights
        sendData["integral_error"] = self.integral_error
        sendData["air_conditioning_signal"] = self.air_conditioning_signal
        sendData["heating_signal"] = self.heating_signal
        sendData["announcements"] = self.next_station
        sendData["time_string"] = self.global_clock.full_text
        sendData["time_multiplier"] = self.global_clock.time_multiplier
        sendData["dt"] = self.global_clock.train_dt
        sendData["kp"] = self.Kp
        sendData["ki"] = self.Ki
        sendData["commanded_power"] = self.commanded_power
        stdin.write(json.dumps(sendData)+'\n')
        # This is to flush stdout
        stdout.readline()
        # This reads in what the pi returns
        piOutput = stdout.readline().rstrip()
        readData = json.loads(piOutput)

        # readDataFormat = ["commanded_power", "emergency_brake",
        #           "service_brake", "left_doors", "right_doors", "headlights",
        #           "interior_lights", "desired_temperature", "manual_mode"]
        self.unramped_commanded_power = readData["commanded_power"]
        self.service_brake = readData["service_brake"]
        self.emergency_brake = readData["emergency_brake"]
        self.left_doors = readData["left_doors"]
        self.right_doors = readData["right_doors"]
        self.headlights = readData["headlights"]
        self.interior_lights = readData["interior_lights"]
        self.desired_temperature = readData["desired_temperature"]
        self.manual_mode = readData["manual_mode"]

