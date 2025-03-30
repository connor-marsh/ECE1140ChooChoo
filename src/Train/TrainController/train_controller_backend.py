"""
Author: Aragya Goyal
Date: 03-20-2025
Description:

"""
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import QTimer, QTime

class TrainController(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set up defaults
        self.actual_speed = 0.0
        self.speed_limit = 0.0
        self.wayside_speed = 0.0
        self.wayside_authority = 0.0
        self.commanded_power = 0.0
        self.passenger_emergency_stop = False
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
        self.door_right = False # Closed default state
        self.door_left = False # Close default state
        self.emergency_brake = False
        self.driver_target_speed = 0.0
        self.service_brake = False
        self.position = 0.0
        self.next_station = ""
        self.announcement = False
        self.manual_mode = False

        # Default for power calculation
        self.integral_error = 0.0
        self.Kp = 500000.0
        self.Ki = 300.0

        # Set up timer for callback/update function
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

        self.deletethistimething = False

    def update(self):
        # Check if auto or manual mode and calculate power
        if (self.manual_mode):
            if (self.driver_target_speed > self.speed_limit):
                # Unsafe
                self.error = self.speed_limit - self.actual_speed
            else:
                # Safe
                self.error = self.driver_target_speed - self.actual_speed
        else:
            # Auto Mode
            if (self.wayside_speed > self.speed_limit):
                # Unsafe
                self.error = self.speed_limit - self.actual_speed
            else:
                # Safe
                self.error = self.wayside_speed - self.actual_speed
            
        self.integral_error += self.error * (0.001) # TODO: THIS SHOULD BE A DT CONSTANT THAT CHANGES THE RATE AT WHICH UPDATE FUNCTION ALSO RUNS
        self.commanded_power = (self.Kp * self.error) + (self.Ki * self.integral_error) # TODO: need something for integral wind up
        # Check authority and stopping distance and override speed calcs
        # TODO

        # Check for invalid power commands
        if (self.commanded_power < 0):
            self.commanded_power = 0.0
            self.service_brake = True
            self.integral_error=0
        elif (self.commanded_power > 120000):
            self.commanded_power = 120000.0
        else:
            self.service_brake = False

        if (self.emergency_brake):
            self.commanded_power = 0.0 # Kill engine if emergency brake is activated
            self.integral_error=0

        # Set the HVAC Signals
        self.air_conditioning_signal = self.actual_temperature > self.desired_temperature
        self.heating_signal = self.actual_temperature < self.desired_temperature

        # Check time for lights
        if (not self.manual_mode):
            if not self.deletethistimething:
                print("FIX TIME THING IN BACKEND END UPDATE AND DELETE VARIABLE")
                self.deletethistimething = True
            hour = 0#self.simulated_time.hour()
            if (hour >= 19 and hour <= 24) or (hour >= 0 and hour < 7):
                self.interior_lights = True
                self.headlights = True
            else:
                self.interior_lights = False
                self.headlights = False

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
            self.speed_limit = selected_data["speed_limit"]
            self.wayside_speed = selected_data["wayside_speed"]
            self.wayside_authority = selected_data["wayside_authority"]
            self.beacon_data = selected_data["beacon_data"]

            # Passengers can turn on the ebrake but not turn it off
            passengerEbrake = selected_data["emergency_brake"]
            if not self.emergency_brake and passengerEbrake:
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
        data["left_doors"] = self.door_left
        data["right_doors"] = self.door_right
        data["interior_lights"] = self.interior_lights
        data["headlights"] = self.headlights
        data["heating_signal"] = self.heating_signal
        data["air_conditioning_signal"] = self.air_conditioning_signal
        data["announcements"] = self.next_station
        return data