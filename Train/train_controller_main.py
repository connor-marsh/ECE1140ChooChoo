"""
Author: Aragya Goyal
Date: 02-16-2025
Description: 

NOTE: When inputting 50 as speed limit display shows sum weird for some reason
"""
import sys
import os
import time
import math

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import QTimer, QTime, QDateTime

from train_controller_ui import Ui_MainWindow as TrainControllerUI
from train_controller_testbench_ui import Ui_TestBenchWindow as TrainControllerTestbenchUI
from train_model_app import TrainModelApp as TrainModel

os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

"""
Helper functions
"""
def speed_conversion(meters_per_second):
    mph = meters_per_second * 2.237
    return mph

def speed_conversion_in(mph):
    meters_per_second = mph / 2.237
    return meters_per_second

def temp_conversion(degree_c):
    degree_f = (degree_c * (9.0/5.0)) + 32.0
    return degree_f

def temp_conversion_in(degree_f):
    degree_c = (degree_f - 32.0) * (5.0/9.0)
    return degree_c

def distance_conversion(meters):
    feet = meters * 3.281
    return feet

def distance_conversion_in(feet):
    pass

"""
Train Controller App
"""
class TrainControllerWindow(QMainWindow):
    def __init__(self, TrainModel):
        # Set up UI for both controller and testbench
        super().__init__()
        self.ui = TrainControllerUI()
        self.ui.setupUi(self)
        self.testbench = TrainControllerTestbenchWindow(self)
        self.model = TrainModel

        # Set up defaults
        self.actual_speed = 0.0
        self.speed_limit = 0.0
        self.commanded_wayside_speed = 0.0
        self.commanded_authority = 0.0
        self.passenger_emergency_stop = False
        self.beacon_data = ""
        self.temperature_status = 25.0 # Celcius
        self.desired_temperature = 25.0 # Celcius
        self.signal_failure = False
        self.brake_failure = False
        self.engine_failure = False
        self.air_conditioning_signal = False
        self.heating_signal = False
        self.headlights = False
        self.interior_lights = False
        self.door_right = False # Closed default state
        self.door_left = False # Close default state
        self.emergency_brake = False
        self.driver_target_speed = 0.0
        self.service_brake = False
        self.position = 0.0
        self.next_station = ""
        self.announcement = False

        # Default for power calculation
        self.integral_error = 0.0
        self.Kp = 1.0
        self.Ki = 1.0
        self.prev_time = None
        self.commanded_power = 0.0

        # Defaults for the UI
        self.ui.cabin_temperature_spin_box.setValue(int(temp_conversion(self.desired_temperature)))

        # Set up buttons to read inputs from UI
        self.ui.control_constants_apply_button.clicked.connect(self.set_k_constants)
        self.ui.headlights_on_button.clicked.connect(self.activate_headlights)
        self.ui.headlights_off_button.clicked.connect(self.deactivate_headlights)
        self.ui.interior_lights_on_button.clicked.connect(self.activate_interior_lights)
        self.ui.interior_lights_off_button.clicked.connect(self.deactivate_interior_lights)
        self.ui.target_speed_apply_button.clicked.connect(self.set_driver_target_speed)

        # Set up the door and emergency buttons to be toggles
        self.ui.door_right_button.setCheckable(True)
        self.ui.door_left_button.setCheckable(True)
        self.ui.emergency_button.setCheckable(True)
        self.ui.door_right_button.toggled.connect(self.handle_right_door)
        self.ui.door_left_button.toggled.connect(self.handle_left_door)
        self.ui.emergency_button.toggled.connect(self.handle_emergency_button)

        # Set up the button to read inputs and set the values from testbench
        self.testbench.ui.tb_input_apply_button.clicked.connect(self.read_testbench_inputs)

        # Set up timer for callback/update function
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

        # Set up timer for updating the clock every second
        self.simulated_time = QTime(6, 59, 0)
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)

    def read_testbench_inputs(self):
        self.actual_speed = self.to_float(self.testbench.ui.tb_actual_speed_line_edit.text())
        self.speed_limit = self.to_float(self.testbench.ui.tb_speed_limit_line_edit.text())
        self.commanded_wayside_speed = self.to_float(self.testbench.ui.tb_commanded_wayside_speed_line_edit.text())
        self.commanded_authority = self.to_float(self.testbench.ui.tb_commanded_wayside_authority_line_edit.text())
        self.passenger_emergency_stop = self.testbench.ui.tb_passenger_emergency_stop_checkbox.isChecked()
        self.beacon_data = self.testbench.ui.tb_beacon_data_line_edit.text()
        self.temperature_status = self.to_float(self.testbench.ui.tb_temperature_status_line_edit.text(), 25.0)
        self.signal_failure = self.testbench.ui.tb_signal_failure_checkbox.isChecked()
        self.brake_failure = self.testbench.ui.tb_brake_failure_checkbox.isChecked()
        self.engine_failure = self.testbench.ui.tb_engine_failure_checkbox.isChecked()
        self.next_station = self.testbench.ui.tb_next_station_line_edit.text()
        self.announcement = self.testbench.ui.tb_announcement_checkbox.isChecked()
    
    def update(self):
        # Get dt based off when this function is being called
        current_time = QDateTime.currentMSecsSinceEpoch()
        if self.prev_time is None:
            self.prev_time = current_time
            return
        dt = (current_time - self.prev_time) / 1000.0  # time step in seconds
        self.prev_time = current_time

        # Set the display values
        self.display_actual_speed(str(speed_conversion(self.actual_speed)))
        self.display_speed_limit(str(speed_conversion(self.speed_limit)))
        self.display_authority(str(distance_conversion(self.commanded_authority)))
        # self.display_cabin_temperature(str(temp_conversion(self.temperature_status)))
        
        # Changes by Iyan:
        # First update desired_temperature from the spinbox:
        self.desired_temperature = temp_conversion_in(self.ui.cabin_temperature_spin_box.value())
        # Then display the setpoint (converted to Fahrenheit)
        self.display_cabin_temperature(str(temp_conversion(self.desired_temperature)))

        # Check if auto or manual mode and calculate power
        if (self.ui.control_mode_switch.value() == 0):
            # Auto Mode
            self.disable_for_auto()
            if (self.commanded_wayside_speed > self.speed_limit):
                # Unsafe
                self.error = self.speed_limit - self.actual_speed
            else:
                # Safe
                self.error = self.commanded_wayside_speed - self.actual_speed
        else:
            # Manual Mode
            self.enable_for_manual()
            if (self.driver_target_speed > self.speed_limit):
                # Unsafe
                self.error = self.speed_limit - self.actual_speed
            else:
                # Safe
                self.error = self.driver_target_speed - self.actual_speed
        self.integral_error += self.error * dt
        self.commanded_power = (self.Kp * self.error) + (self.Ki * self.integral_error) # TODO: need something for integral wind up
        
        # Check for invalid power commands
        if (self.commanded_power < 0):
            self.commanded_power = 0.0
            self.integral_error = 0.0
            self.activate_service_brake()
        elif (self.commanded_power > 120000):
            self.commanded_power = 120000.0
            self.deactivate_service_brake()
        else:
            self.deactivate_service_brake()

        if (self.emergency_brake):
            self.commanded_power = 0.0 # Kill engine if emergency brake is toggled
        self.display_commanded_power(self.commanded_power)

        # Set Emergency Lights and handle emergency brakes
        self.activate_signal_failure() if self.signal_failure else self.deactivate_signal_failure()
        self.activate_brake_failure() if self.brake_failure else self.deactivate_brake_failure()
        self.activate_engine_failure() if self.engine_failure else self.deactivate_engine_failure()
        if self.passenger_emergency_stop:
            self.activate_emergency_brake()

        # Set the HVAC Signals
        self.desired_temperature = temp_conversion_in(self.ui.cabin_temperature_spin_box.value())
        self.activate_air_conditioning() if self.temperature_status > self.desired_temperature else self.deactivate_air_conditioning()
        self.activate_heating() if self.temperature_status < self.desired_temperature else self.deactivate_heating()

        # Check time for lights
        if (self.ui.control_mode_switch.value() == 0):
            hour = self.simulated_time.hour()
            if (hour >= 19 and hour <= 24) or (hour >= 0 and hour < 7):
                self.activate_interior_lights()
                self.activate_headlights()
            else:
                self.deactivate_interior_lights()
                self.deactivate_headlights()

        if (self.actual_speed > 0):
            self.ui.door_left_button.setEnabled(False)
            self.ui.door_right_button.setEnabled(False)
            self.door_right = False
            self.door_left = False

        # Set next station and on air light
        self.display_next_station()
        self.activate_announcement_light() if self.announcement else self.deactivate_announcement_light()
    
    def activate_announcement_light(self):
        self.ui.announcement_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")

    def deactivate_announcement_light(self):
        self.ui.announcement_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")

    def display_next_station(self):
        self.ui.next_station_label.setText(self.next_station)

    def activate_service_brake(self):
        self.service_brake = True
        self.ui.service_brake_on_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")
        self.ui.service_brake_off_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")

    def deactivate_service_brake(self):
        self.service_brake = False
        self.ui.service_brake_on_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
        self.ui.service_brake_off_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")

    def set_driver_target_speed(self):
        self.driver_target_speed = speed_conversion_in(self.ui.target_speed_spin_box.value()) # TODO: needs to be converted to m/s
        self.ui.target_speed_lcd.display(speed_conversion(self.driver_target_speed))

    def display_commanded_power(self, power):
        self.ui.commanded_power_lcd.display(power)

    def display_cabin_temperature(self, temperature):
        self.ui.cabin_temperature_lcd.display(temperature)

    def display_authority(self, authority):
        self.ui.authority_lcd.display(authority)

    def display_speed_limit(self, speed_limit):
        self.ui.speed_limit_lcd.display(speed_limit)

    def display_actual_speed(self, speed):
        self.ui.actual_speed_lcd.display(speed)

    def disable_for_auto(self):
        self.ui.target_speed_apply_button.setEnabled(False)
        self.ui.interior_lights_on_button.setEnabled(False)
        self.ui.interior_lights_off_button.setEnabled(False)
        self.ui.headlights_on_button.setEnabled(False)
        self.ui.headlights_off_button.setEnabled(False)

    def enable_for_manual(self):
        self.ui.target_speed_apply_button.setEnabled(True)
        self.ui.door_left_button.setEnabled(True)
        self.ui.door_right_button.setEnabled(True)
        self.ui.interior_lights_on_button.setEnabled(True)
        self.ui.interior_lights_off_button.setEnabled(True)
        self.ui.headlights_on_button.setEnabled(True)
        self.ui.headlights_off_button.setEnabled(True)

    def handle_emergency_button(self, checked):
        # if checked:
        #     self.emergency_brake = True
        # else:
        #     self.emergency_brake = False
        #     self.passenger_emergency_stop = False
        if checked:
            self.model.emergency_source = "controller"
            self.model.set_emergency_state(True)
        else:
            self.model.emergency_source = None
            self.model.set_emergency_state(False)
    
    def activate_emergency_brake(self):
        self.ui.emergency_button.setChecked(True)

    def handle_right_door(self, checked):
        if checked:
            self.door_right = True
        else:
            self.door_right = False

    def handle_left_door(self, checked):
        if checked:
            self.door_left = True
        else:
            self.door_left = False

    def activate_headlights(self):
        self.headlights = True

    def deactivate_headlights(self):
        self.headlights = False

    def activate_interior_lights(self):
        self.interior_lights = True

    def deactivate_interior_lights(self):
        self.interior_lights = False

    def activate_heating(self):
        self.heating_signal = True

    def deactivate_heating(self):
        self.heating_signal = False

    def activate_air_conditioning(self):
        self.air_conditioning_signal = True
    
    def deactivate_air_conditioning(self):
        self.air_conditioning_signal = False

    def set_k_constants(self):
        self.Kp = self.to_float(self.ui.kp_line_edit.text(), 1.0)
        self.Ki = self.to_float(self.ui.ki_line_edit.text(), 1.0)
        self.ui.control_constants_apply_button.setEnabled(False)
        self.ui.kp_line_edit.setEnabled(False)
        self.ui.ki_line_edit.setEnabled(False)

    def activate_signal_failure(self):
        self.ui.signal_failure_light.setStyleSheet("background-color: red; font-weight: bold; font-size: 16px;")

    def deactivate_signal_failure(self):
        self.ui.signal_failure_light.setStyleSheet("background-color: rgb(255, 170, 170); font-weight: bold; font-size: 16px;")

    def activate_brake_failure(self):
        self.ui.brake_failure_light.setStyleSheet("background-color: red; font-weight: bold; font-size: 16px;")
    
    def deactivate_brake_failure(self):
        self.ui.brake_failure_light.setStyleSheet("background-color: rgb(255, 170, 170); font-weight: bold; font-size: 16px;")

    def activate_engine_failure(self):
        self.ui.engine_failure_light.setStyleSheet("background-color: red; font-weight: bold; font-size: 16px;")

    def deactivate_engine_failure(self):
        self.ui.engine_failure_light.setStyleSheet("background-color: rgb(255, 170, 170); font-weight: bold; font-size: 16px;")

    def update_clock(self):
        # Add one second to the simulated time
        self.simulated_time = self.simulated_time.addSecs(1)

        # Extract hour, minute, second from the simulated time
        hour = self.simulated_time.hour()
        minute = self.simulated_time.minute()
        second = self.simulated_time.second()

        # Convert to 12-hour format and set AM/PM
        am_pm = "AM" if hour < 12 else "PM"
        hour_12 = hour % 12
        if hour_12 == 0:
            hour_12 = 12

        # Format the time as HH:MM:SS
        time_text = f"{hour_12:02d}:{minute:02d}:{second:02d}"

        # Update the clock LCD and the AM/PM label
        self.ui.global_clock_lcd.display(time_text)
        self.ui.am_pm_label.setText(am_pm)
    
    def to_float(self, val_str, default=0.0):
        # Helper for string->float conversion
        try:
            return float(val_str)
        except ValueError:
            return default

"""
Train Controller Testbench
"""
class TrainControllerTestbenchWindow(QMainWindow):
    def __init__(self, train_controller_window):
        super().__init__()
        self.ui = TrainControllerTestbenchUI()
        self.ui.setupUi(self)
        self.train_controller_window = train_controller_window

        # Set up timer for callback/update function
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_testbench)
        self.timer.start(100)

    def update_testbench(self):
        self.display_air_conditioning()
        self.display_heating()
        self.display_headlights()
        self.display_internal_lights()
        self.display_doors()
        self.display_emergency_brakes()
        self.display_service_brakes()
        self.display_announcement()

    def display_announcement(self):
        if (self.train_controller_window.announcement):
            self.ui.tb_annunciation_system_display.setText(self.train_controller_window.next_station)

    def display_service_brakes(self):
        if (self.train_controller_window.service_brake):
            self.ui.tb_service_brakes_on_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")
            self.ui.tb_service_brakes_off_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
        else:
            self.ui.tb_service_brakes_on_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
            self.ui.tb_service_brakes_off_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")

    def display_emergency_brakes(self):
        if (self.train_controller_window.emergency_brake):
            self.ui.tb_emergency_brake_on_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")
            self.ui.tb_emergency_brake_off_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
        else:
            self.ui.tb_emergency_brake_on_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
            self.ui.tb_emergency_brake_off_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")

    def display_headlights(self):
        if (self.train_controller_window.headlights):
            self.ui.tb_headlight_on_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")
            self.ui.tb_headlight_off_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
        else:
            self.ui.tb_headlight_on_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
            self.ui.tb_headlight_off_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")

    def display_internal_lights(self):
        if (self.train_controller_window.interior_lights):
            self.ui.tb_internal_light_on_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")
            self.ui.tb_internal_light_off_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
        else:
            self.ui.tb_internal_light_on_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
            self.ui.tb_internal_light_off_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")

    def display_air_conditioning(self):
        if (self.train_controller_window.air_conditioning_signal):
            self.ui.tb_air_conditioning_on_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")
            self.ui.tb_air_conditioning_off_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
        else:
            self.ui.tb_air_conditioning_on_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
            self.ui.tb_air_conditioning_off_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")

    def display_heating(self):
        if (self.train_controller_window.heating_signal):
            self.ui.tb_heating_signal_on_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")
            self.ui.tb_heating_signal_off_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
        else:
            self.ui.tb_heating_signal_on_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
            self.ui.tb_heating_signal_off_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")

    def display_doors(self):
        if (self.train_controller_window.door_right):
            self.ui.tb_right_door_open_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")
            self.ui.tb_right_door_close_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
        else:
            self.ui.tb_right_door_open_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
            self.ui.tb_right_door_close_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")

        if (self.train_controller_window.door_left):
            self.ui.tb_left_door_open_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")
            self.ui.tb_left_door_close_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
        else:
            self.ui.tb_left_door_open_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
            self.ui.tb_left_door_close_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")

"""
Main
"""
def main():
    app = QApplication(sys.argv)
    train_controller_window = TrainControllerWindow()
    train_controller_window.show()
    # train_controller_window.testbench.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()