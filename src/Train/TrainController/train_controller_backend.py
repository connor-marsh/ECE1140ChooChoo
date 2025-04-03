"""
Author: Aragya Goyal and Connor Marsh
Date: 03-20-2025
Description:

"""
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer
import globals.global_clock as global_clock

class TrainController(QMainWindow):
    def __init__(self, train_integrated=True):
        super().__init__()

        # Set up defaults
        self.actual_speed = 0.0
        self.speed_limit = 20.0
        self.wayside_speed = 0.0
        self.wayside_authority = 0.0
        self.commanded_power = 0.0
        self.beacon_data = ""
        self.actual_temperature = 77.0 # Farenheight
        self.desired_temperature = 77.0 # Farenheight
        self.signal_failure = False
        self.brake_failure = False
        self.engine_failure = False
        self.air_conditioning_signal = False
        self.heating_signal = False
        self.headlights = False
        self.interior_lights = False
        self.right_doors = False # Closed default state
        self.left_doors = False # Close default state
        self.emergency_brake = False
        self.driver_target_speed = 0.0
        self.service_brake = False
        self.position = 0.0
        self.next_station = ""
        self.announcement = False
        self.manual_mode = False
        self.target_speed = 0.0

        # Default for power calculation
        self.integral_error = 0.0
        self.Kp = 20000.0
        self.Ki = 75.0

        self.global_clock = global_clock.clock

        if not train_integrated:
            # Set up timer for callback/update function
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update)
            self.timer.start(self.global_clock.train_dt)


    def update(self):
        self.update_power()
        self.update_safety()
        self.update_auxiliary()

    def update_power(self):
        # Check if auto or manual mode and calculate power
        if self.manual_mode:
            self.target_speed = self.driver_target_speed
        else:
            self.target_speed = self.wayside_speed
        self.target_speed = min(self.target_speed, self.speed_limit*0.9)

        self.error = self.target_speed - self.actual_speed
        self.integral_error += self.error * self.global_clock.train_dt/1000 * self.global_clock.time_multiplier
        commanded_power_1 = (self.Kp * self.error) + (self.Ki * self.integral_error)
        commanded_power_2 = (self.Kp * self.error) + (self.Ki * self.integral_error)
        commanded_power_3 = (self.Kp * self.error) + (self.Ki * self.integral_error)
        if (commanded_power_1 == commanded_power_2 and commanded_power_1 == commanded_power_3 and commanded_power_2 == commanded_power_3):
            self.commanded_power = commanded_power_1
        else:
            self.commanded_power = 0
    def update_safety(self):

        # Check for failures
        if (self.signal_failure or self.brake_failure or self.engine_failure):
            self.emergency_brake = True

        # TODO: Check authority and stopping distance and override speed calcs

        # Check for invalid power commands
        new_service_state = False
        if (self.commanded_power <= 0):
            self.commanded_power = 0.0
            new_service_state = True
        elif (self.commanded_power > 120000):
            self.commanded_power = 120000.0
        
        if not self.manual_mode:
            self.service_brake=new_service_state

        if (self.emergency_brake):
            self.commanded_power = 0.0 # Kill engine if emergency brake is activated
            self.integral_error = 0

        if (self.service_brake):
            self.commanded_power = 0.0 # Kill engine if emergency brake is activated
            self.integral_error = 0
    def update_auxiliary(self):
        # Set the HVAC Signals
        self.air_conditioning_signal = self.actual_temperature > self.desired_temperature
        self.heating_signal = self.actual_temperature < self.desired_temperature

        # Check time for lights
        if (not self.manual_mode):
            if (self.global_clock.hour >= 19 and self.global_clock.hour <= 24) or (self.global_clock.hour >= 0 and self.global_clock.hour < 7):
                self.interior_lights = True
                self.headlights = True
            else:
                self.interior_lights = False
                self.headlights = False

        # Close doors if we are moving
        if (self.actual_speed > 0):
            self.left_doors = False
            self.right_doors = False

        # check underground for lights
        # TODO

        # check for stopping at stations/do announcements
        # TODO

    def set_input_data(self, testbench_data=None, train_model_data=None):
        selected_data = None
        selected = ""

        if testbench_data:
            selected_data = testbench_data
            selected = "testbench"
        elif train_model_data:
            selected_data = train_model_data
            selected = "train_model"

        if selected == "testbench" or selected == "train_model":
            self.actual_speed = selected_data["actual_speed"]
            self.wayside_speed = selected_data["wayside_speed"]
            self.wayside_authority = selected_data["wayside_authority"]
            self.beacon_data = selected_data["beacon_data"]

            # Passengers can turn on the ebrake but not turn it off
            passengerEbrake = selected_data.get("emergency_brake", False)
            if passengerEbrake:
                self.emergency_brake = True

            self.actual_temperature = selected_data["actual_temperature"]
            self.signal_failure = selected_data["signal_failure"]
            self.brake_failure = selected_data["brake_failure"]
            self.engine_failure = selected_data["engine_failure"]

    def get_output_data(self):
        data = {}
        data["commanded_power"] = self.commanded_power
        data["service_brake"] = self.service_brake
        data["emergency_brake"] = self.emergency_brake
        data["left_doors"] = self.left_doors
        data["right_doors"] = self.right_doors
        data["interior_lights"] = self.interior_lights
        data["headlights"] = self.headlights
        data["heating_signal"] = self.heating_signal
        data["air_conditioning_signal"] = self.air_conditioning_signal
        data["announcements"] = self.next_station
        return data