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
sendDataFormat = ["actual_speed", "wayside_speed", "wayside_authority", "emergency_brake",
                  "actual_temperature", "brake_failure", "engine_failure", "signal_failure",
                  "service_brake", "left_doors", "right_doors", "headlights",
                  "interior_lights", "air_conditioning_signal", "heating_signal", "announcements"]

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
        self.update_safety()
        self.update_auxiliary()

    def update_hardware(self):
        # Send data to and retrive data from raspi
        # Raspi does the power calculation, and has a hardware UI, and thats it
        # sendDataFormat = ["actual_speed", "wayside_speed", "wayside_authority", "emergency_brake",
        #           "actual_temperature", "brake_failure", "engine_failure", "signal_failure",
        #           "service_brake", "left_doors", "right_doors", "headlights",
        #           "interior_lights", "air_conditioning_signal", "heating_signal", "announcements"]
        sendData["actual_speed"] = self.actual_speed
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
        stdin.write(json.dumps(sendData)+'\n')
        # This is to flush stdout
        stdout.readline()
        # This reads in what the pi returns
        readData = json.loads(stdout.readline().rstrip())

        # readDataFormat = ["commanded_power", "emergency_brake",
        #           "service_brake", "left_doors", "right_doors", "headlights",
        #           "interior_lights", "desired_temperature", "manual_mode"]
        self.commanded_power = readData["commanded_power"]
        self.service_brake = readData["service_brake"]
        self.emergency_brake = readData["emergency_brake"]
        self.left_doors = readData["left_doors"]
        self.right_doors = readData["right_doors"]
        self.headlights = readData["headlights"]
        self.interior_lights = readData["interior_lights"]
        self.desired_temperature = readData["desired_temperature"]
        self.manual_mode = readData["manual_mode"]




# """
# Train Controller App
# """
# class TrainControllerWindow(QMainWindow):
#     def __init__(self):
#         # Set up UI for both controller and testbench
#         super().__init__()
#         # self.ui = TrainControllerUI()
#         # self.ui.setupUi(self)
#         self.testbench = TrainControllerTestbenchWindow(self)

#         # Set up defaults
#         self.actual_speed = 0.0
#         self.speed_limit = 0.0
#         self.commanded_wayside_speed = 0.0
#         self.commanded_authority = 0.0
#         self.commanded_power = 0.0
#         self.passenger_emergency_stop = False
#         self.beacon_data = ""
#         self.temperature_status = 25.0 # Celcius
#         self.desired_temperature = 25.0 # Celcius
#         self.signal_failure = False
#         self.brake_failure = False
#         self.engine_failure = False
#         self.air_conditioning_signal = False
#         self.heating_signal = False
#         self.headlights = False
#         self.interior_lights = False
#         self.right_doors = False # Closed default state
#         self.left_doors = False # Close default state
#         self.emergency_brake = False
#         self.driver_target_speed = 0.0
#         self.service_brake = False
#         self.position = 0.0
#         self.next_station = "Edgebrook"

#         # Default for power calculation
#         self.integral_error = 0.0
#         self.Kp = 1.0
#         self.Ki = 1.0

        
#         self.testbench.ui.tb_input_apply_button.clicked.connect(self.read_testbench_inputs)

#         # Set up timer for callback/update function
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.update)
#         self.timer.start(100)

#         # Set up timer for updating the clock every second
#         # self.simulated_time = QTime(6, 59, 0)
#         # self.clock_timer = QTimer(self)
#         # self.clock_timer.timeout.connect(self.update_clock)
#         # self.clock_timer.start(1000)

#     def read_testbench_inputs(self):
#         self.actual_speed = self.to_float(self.testbench.ui.tb_actual_speed_line_edit.text())
#         self.speed_limit = self.to_float(self.testbench.ui.tb_speed_limit_line_edit.text())
#         self.commanded_wayside_speed = self.to_float(self.testbench.ui.tb_commanded_wayside_speed_line_edit.text())
#         self.commanded_authority = self.to_float(self.testbench.ui.tb_commanded_wayside_authority_line_edit.text())
#         self.passenger_emergency_stop = self.testbench.ui.tb_passenger_emergency_stop_checkbox.isChecked()
#         self.beacon_data = self.testbench.ui.tb_beacon_data_line_edit.text()
#         self.temperature_status = self.to_float(self.testbench.ui.tb_temperature_status_line_edit.text(), 25.0)
#         self.signal_failure = self.testbench.ui.tb_signal_failure_checkbox.isChecked()
#         self.brake_failure = self.testbench.ui.tb_brake_failure_checkbox.isChecked()
#         self.engine_failure = self.testbench.ui.tb_engine_failure_checkbox.isChecked()
    
#     def update(self):
#         # collect data to send based off internal data from testbench
#         #sendDataFormat = ["actual_speed", "commanded_speed", "authority", "ebrake_state", "temperature", "brake_failure", "engine_failure", "signal_failure"]
#         sendData["actual_speed"] = self.actual_speed
#         sendData["commanded_speed"] = self.commanded_wayside_speed
#         sendData["authority"] = self.commanded_authority
#         sendData["ebrake_state"] = self.passenger_emergency_stop
#         sendData["temperature"] = self.temperature_status
#         sendData["brake_failure"] = self.brake_failure
#         sendData["engine_failure"] = self.engine_failure
#         sendData["signal_failure"] = self.signal_failure
#         stdin.write(json.dumps(sendData)+'\n')
#         stdout.readline()
#         readData = json.loads(stdout.readline().rstrip())
#         self.commanded_power = readData["commanded_power"]
#         self.service_brake = readData["brakes"]
#         self.passenger_emergency_stop = self.emergency_brake = readData["ebrake"]
#         self.left_doors = readData["left_doors"]
#         self.right_doors = readData["right_doors"]
#         self.headlights = readData["headlights"]
#         self.interior_lights = readData["lights"]
#         self.air_conditioning_signal = readData["ac"]
#         self.heating_signal = readData["heat"]
#         self.next_station = readData["annunciation"]

    
    
#     def to_float(self, val_str, default=0.0):
#         # Helper for string->float conversion
#         try:
#             return float(val_str)
#         except ValueError:
#             return default



# """
# Main
# """
# def main():
#     app = QApplication(sys.argv)
#     train_controller_window = TrainControllerWindow()
#     train_controller_window.show()
#     train_controller_window.testbench.show()
#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     main()