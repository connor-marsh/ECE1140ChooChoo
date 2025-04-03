"""
Author: Iyan Nekib
Date: 03-20-2025
Description:

"""

# backend.py
import math
import os
import sys
import time
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtCore import QTimer, QTime, QDateTime

from Train.TrainController.train_controller_backend import TrainController
from Train.TrainController.train_controller_hw_backend import TrainControllerHW
import globals.global_clock as global_clock

class TrainModel(QMainWindow):
    # Conversion factors and constants.
    MPS_TO_MPH  = 2.23694
    KG_TO_LBS   = 2.20462
    M_TO_FT     = 3.281

    MAX_ACCEL         = 100000    # (m/s²)
    GRAVITY           = 9.81      # (m/s²)
    EMERGENCY_DECEL   = -2.73     # (m/s²)
    SERVICE_DECEL     = -1.2      # (m/s²)
    MIN_SPEED_NO_BRAKE= 0.1       # (m/s)
    
    # Coefficients for drag force calculation.
    DRAG_COEFFICIENT = 1.2    # Example value; tune based on actual train data.
    FRONTAL_AREA = 9.06       # Frontal Area calculated from train dimensions --> (Width * Height) in m².
    AIR_DENSITY = 1.225       # kg/m³ at sea level.

    def __init__(self, train_integrated=True, hardware_controller=False):
        super().__init__()
        if train_integrated:
            if hardware_controller:
                self.controller = TrainControllerHW()
            else:
                self.controller = TrainController()
        else:
            self.controller = None
        self.position = 0.0
        self.actual_speed = 0.0
        self.current_acceleration = 0.0
        self.previous_acceleration = 0.0
        self.actual_temperature = 25  # Celsius

        self.commanded_power = 0
        self.service_brake = False
        self.emergency_brake = False
        self.send_emergency_brake_signal = False
        self.cabin_lights = False
        self.headlights = False
        self.left_doors = False
        self.right_doors = False
        self.announcement = ""
        self.heating = False
        self.air_conditioning = False

        self.wayside_speed = 0
        self.wayside_authority = 0
        self.beacon_data = ""

        self.mass_kg = 37103.86
        self.crew_count = 2.0
        self.length_m = 32.2
        self.height_m = 3.42
        self.width_m = 2.65
        self.grade = 0.0  # percent
        self.passenger_count = 0 

        self.brake_failure = False
        self.signal_failure = False
        self.engine_failure = False

        self.global_clock = global_clock.clock

        self.prev_time = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(self.global_clock.train_dt)

        # Ensure a backend attribute exists.
        self.backend = self

    def update(self):
        if self.controller:
            self.controller.set_input_data(train_model_data=self.get_output_data())
            self.controller.update()
            self.set_input_data(train_controller_data=self.controller.get_output_data())
        current_time = QDateTime.currentMSecsSinceEpoch()
        if self.prev_time is None:
            self.prev_time = current_time
            return
        dt = (current_time - self.prev_time) / 1000.0 * self.global_clock.time_multiplier
        self.prev_time = current_time

        try:
            v_eff = self.actual_speed if self.actual_speed > 0.001 else 0.001
            dyn_force = self.commanded_power / v_eff
        except ZeroDivisionError:
            dyn_force = 1000.0

        theta = math.atan(self.grade / 100.0)
        grav_force = self.mass_kg * self.GRAVITY * math.sin(theta)
        
        """Calculate drag force using the drag equation.
            drag_force = 0.5 * rho * A * C_d * v^2 """
        # air_resistance_constant = 20
        velocity_magnitude = math.sqrt(self.actual_speed**2 + self.actual_speed**2) # Calculate velocity magnitude
        drag_force = 0.5 * self.AIR_DENSITY * self.FRONTAL_AREA * self.DRAG_COEFFICIENT * velocity_magnitude**2
        # net_force = dyn_force - grav_force * air_resistance_constant
        net_force = dyn_force - grav_force - drag_force     # TODO: Make drag code more clean
        a_base = net_force / self.mass_kg if self.mass_kg != 0 else 0.0

        if self.emergency_brake:
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
        # Calculate new velocity using the trapezoidal rule.
        new_velocity = old_velocity + (dt / 2.0) * (final_acceleration + self.previous_acceleration)
        # Calculate new position using the trapezoidal rule.
        new_position = self.position + (dt / 2.0) * (old_velocity + new_velocity)
        self.position = new_position
        
        # Check for overspeed and adjust velocity if necessary.
        if new_velocity < 0:
            new_velocity = 0

        # Clamp the speed to a maximum of 43.49 mph (≈19.44 m/s)
        max_speed_mps = 43.49 / self.MPS_TO_MPH
        if new_velocity > max_speed_mps:
            new_velocity = max_speed_mps

        self.previous_acceleration = final_acceleration
        self.actual_speed = new_velocity
        self.current_acceleration = final_acceleration

        brake_off = (not self.emergency_brake) and (not self.service_brake)
        if brake_off and new_velocity < self.MIN_SPEED_NO_BRAKE:
            new_velocity = self.MIN_SPEED_NO_BRAKE

        degrees_per_second = 0.001
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

    def set_input_data(self, testbench_data=None, track_data=None, train_controller_data=None):
        selected_data = None
        selected = ""
        if testbench_data:
            selected_data = testbench_data
            selected = "testbench"
        elif track_data:
            selected_data = track_data
            selected = "track"
        elif train_controller_data:
            selected_data = train_controller_data
            selected = "train_controller"

        if selected in ["testbench", "track"]:
            self.wayside_speed = selected_data.get("wayside_speed", self.wayside_speed) / self.MPS_TO_MPH
            self.wayside_authority = selected_data.get("wayside_authority", self.wayside_authority) / self.M_TO_FT
            self.beacon_data = selected_data.get("beacon_data", self.beacon_data)
            grade = selected_data.get("grade", self.grade)
            if grade > 60:
                grade = 60.0
            elif grade < 0:
                grade = 0.0
            self.grade = grade
            self.passenger_count = selected_data.get("passenger_count", self.passenger_count)
            self.crew_count = selected_data.get("crew_count", self.crew_count)
            self.mass_kg = 37103.86 + (self.passenger_count * 70) + (self.crew_count * 70)
            
        if selected in ["testbench", "train_controller"]:
            commanded_power = selected_data.get("commanded_power", self.commanded_power)
            if commanded_power > 120000:
                commanded_power = 120000.0
            elif commanded_power < 0:
                commanded_power = 0.0
            self.commanded_power = commanded_power

            self.service_brake = selected_data.get("service_brake", self.service_brake)
            self.emergency_brake = selected_data.get("emergency_brake", self.emergency_brake)
            self.cabin_lights = selected_data.get("interior_lights", self.cabin_lights)
            self.headlights = selected_data.get("headlights", self.headlights)
            self.left_doors = selected_data.get("left_doors", self.left_doors)
            self.right_doors = selected_data.get("right_doors", self.right_doors)
            self.announcement = selected_data.get("announcements", self.announcement)
            self.heating = selected_data.get("heating_signal", self.heating)
            self.air_conditioning = selected_data.get("air_conditioning_signal", self.air_conditioning)

    def get_output_data(self):
        data = {}
        data["actual_speed"] = self.actual_speed * self.MPS_TO_MPH
        data["wayside_speed"] = self.wayside_speed * self.MPS_TO_MPH
        data["wayside_authority"] = self.wayside_authority * self.M_TO_FT
        data["beacon_data"] = self.beacon_data
        data["actual_temperature"] = (self.actual_temperature * 1.8) + 32
        data["signal_failure"] = self.signal_failure
        data["brake_failure"] = self.brake_failure
        data["engine_failure"] = self.engine_failure
        data["position"] = self.position * self.M_TO_FT
        if self.send_emergency_brake_signal:
            data["emergency_brake"] = self.emergency_brake
            self.send_emergency_brake_signal = False
        return data