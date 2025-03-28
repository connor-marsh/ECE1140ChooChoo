# backend.py

import math
import os
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import QTimer, QTime, QDateTime

current_dir = os.path.dirname(__file__)
train_dir = os.path.abspath(os.path.join(current_dir, "../TrainController"))
sys.path.insert(0, train_dir)

class TrainModel(QMainWindow):
    # Conversion factors and constants
    MPS_TO_MPH  = 2.23694
    KG_TO_LBS   = 2.20462
    M_TO_FT     = 3.281

    MAX_ACCEL         = 100000    # (m/s²)
    GRAVITY           = 9.81      # (m/s²)
    EMERGENCY_DECEL   = -2.73     # (m/s²)
    SERVICE_DECEL     = -1.2      # (m/s²)
    MIN_SPEED_NO_BRAKE= 0.1       # (m/s)

    def __init__(self):
        super().__init__()
        
        # internal values
        if __name__ == "__main__":
            self.controller = None
        else:
            from train_controller_backend import TrainController
            self.controller = TrainController()
        self.position = 0.0
        self.actual_speed = 0.0
        self.current_acceleration = 0.0
        self.previous_acceleration = 0.0
        self.actual_temperature = 25  # in Celsius

        # communicated values: Train Controller
        self.commanded_power = 0
        self.service_brake = False
        self.driver_emergency_brake = False
        self.cabin_lights = False
        self.headlights = False
        self.left_doors = False
        self.right_doors = False
        self.announcement = ""
        self.heating = False
        self.air_conditioning = False

        # communicated values: Track Model
        self.wayside_speed = 0
        self.wayside_authority = 0
        self.beacon_data = ""

        # Additional physical properties (defaults)
        self.mass_kg = 37103.86
        self.crew_count = 2.0
        self.length_m = 32.2
        self.height_m = 3.42
        self.width_m = 2.65
        self.grade = 0.0 # percent
        self.passenger_count = 0 
        self.speed_limit = 0.0 # m/s

        # Failure flags
        self.brake_failure = False
        self.signal_failure = False
        self.engine_failure = False
        
        # Set up timer for callback/update function
        self.prev_time = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

        # Minimal fix: Ensure a backend attribute exists.
        self.backend = self

    def update(self):

        if __name__ != "__main__":
            self.controller.set_input_data(train_model_data=self.get_output_data())
            self.controller.update()
            self.set_input_data(train_controller_data=self.controller.get_output_data())
        
        # if self.current_train:
        current_time = QDateTime.currentMSecsSinceEpoch()
        if self.prev_time is None:
            self.prev_time = current_time
            return
        dt = (current_time - self.prev_time) / 1000.0
        self.prev_time = current_time

        try:
            v_eff = self.actual_speed if self.actual_speed > 0.001 else 0.001
            dyn_force = self.commanded_power / v_eff
        except ZeroDivisionError:
            dyn_force = 1000.0

        theta = math.atan(self.grade / 100.0)
        grav_force = self.mass_kg * self.GRAVITY * math.sin(theta)
        net_force = dyn_force - grav_force
        a_base = net_force / self.mass_kg if self.mass_kg != 0 else 0.0

        if self.driver_emergency_brake:
            target_a = self.EMERGENCY_DECEL - self.GRAVITY * math.sin(theta)
            self.current_acceleration = target_a
        elif self.service_brake:
            target_a = self.SERVICE_DECEL - self.GRAVITY * math.sin(theta)
            ramp_rate = 1.0
            accel_diff = target_a - self.current_acceleration
            max_delta = ramp_rate * dt
            if abs(accel_diff) < max_delta:
                self.current_acceleration = target_a
            else:
                self.current_acceleration += math.copysign(max_delta, accel_diff)
        else:
            target_a = a_base
            ramp_rate = 1.0
            accel_diff = target_a - self.current_acceleration
            max_delta = ramp_rate * dt
            if abs(accel_diff) < max_delta:
                self.current_acceleration = target_a
            else:
                self.current_acceleration += math.copysign(max_delta, accel_diff)

        final_acceleration = self.current_acceleration
        if final_acceleration > self.MAX_ACCEL:
            final_acceleration = self.MAX_ACCEL
        elif final_acceleration < -self.MAX_ACCEL:
            final_acceleration = -self.MAX_ACCEL

        old_velocity = self.actual_speed
        new_velocity = old_velocity + (dt / 2.0) * (final_acceleration + self.previous_acceleration)
        if new_velocity < 0:
            new_velocity = 0

        self.previous_acceleration = final_acceleration
        self.actual_speed = new_velocity
        self.current_acceleration = final_acceleration

        brake_off = (not self.driver_emergency_brake) and (not self.service_brake)
        if brake_off and new_velocity < self.MIN_SPEED_NO_BRAKE:
            new_velocity = self.MIN_SPEED_NO_BRAKE

        # Temperature control logic
        degrees_per_second = 0.05
        if self.heating and not self.air_conditioning:
            dtemp = degrees_per_second * dt
        elif self.air_conditioning and not self.heating:
            dtemp = -degrees_per_second * dt
        elif self.air_conditioning and self.heating:
            dtemp = 0.0
        else:
            dtemp = 0.0001
        self.actual_temperature += dtemp
        display_temp = (self.actual_temperature * 1.8) + 32

        return {
            "acceleration": final_acceleration,
            "velocity": new_velocity,
            "actual_temperature": display_temp
        }
    
    def set_input_data(self, testbench_data=None, wayside_data=None, train_controller_data=None):
        selected_data = None
        selected = ""

        if testbench_data:
            selected_data = testbench_data
            selected = "testbench"
        elif wayside_data:
            selected_data = wayside_data
            selected = "wayside"
        elif train_controller_data:
            selected_data = train_controller_data
            selected = "train_controller"

        if selected == "testbench" or selected == "wayside":
            self.wayside_speed = selected_data["commanded_speed"]
            self.wayside_authority = selected_data["authority"]
            self.beacon_data = selected_data["beacon_data"]
        
        if selected == "testbench" or selected == "train_controller":
            # clamo the commanded power to 120kW
            commanded_power = selected_data.get("commanded_power", self.commanded_power)
            if commanded_power > 120000:
                commanded_power = 120000.0
            elif commanded_power < 0:
                commanded_power = 0.0
            self.commanded_power = commanded_power

            self.service_brake = selected_data.get("service_brake", self.service_brake)
            self.driver_emergency_brake = selected_data.get("emergency_brake", self.driver_emergency_brake)
            self.cabin_lights = selected_data.get("interior_lights", self.cabin_lights)
            self.headlights = selected_data.get("headlights", self.headlights)
            self.left_doors = selected_data.get("left_doors", self.left_doors)
            self.right_doors = selected_data.get("right_doors", self.right_doors)
            self.announcement = selected_data.get("announcements", self.announcement)
            self.heating = selected_data.get("heating_signal", self.heating)
            self.air_conditioning = selected_data.get("air_conditioning_signal", self.air_conditioning)
            
            # update physical properties from testbench input.
            grade = selected_data.get("grade", self.grade)
            if grade > 60:
                grade = 60.0
            elif grade < 0:
                grade = 0.0
            self.grade = grade
            self.passenger_count = selected_data.get("passenger_count", self.passenger_count)
            
            # update mass_kg based on passenger count
            self.crew_count = selected_data.get("crew_count", self.crew_count)
            self.mass_kg = 37103.86 + (self.passenger_count * 70) + (self.crew_count * 70)
            
            # self.mass_kg = selected_data.get("mass_kg", self.mass_kg)
            # self.length_m = selected_data.get("length_m", self.length_m)
            # self.height_m = selected_data.get("height_m", self.height_m)
            # self.width_m = selected_data.get("width_m", self.width_m)
            self.speed_limit = selected_data.get("speed_limit", self.speed_limit)
    def get_output_data(self):
        data = {}
        data["actual_speed"] = self.actual_speed
        data["wayside_speed"] = self.wayside_speed
        data["wayside_authority"] = self.wayside_authority
        data["beacon_data"] = self.beacon_data
        data["actual_temperature"] = self.actual_temperature
        data["signal_failure"] = self.signal_failure
        data["brake_failure"] = self.brake_failure
        data["engine_failure"] = self.engine_failure
        data["speed_limit"] = self.speed_limit
        data["emergency_brake"] = self.driver_emergency_brake
        return data