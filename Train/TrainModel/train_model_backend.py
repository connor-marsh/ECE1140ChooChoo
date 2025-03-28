# backend.py

import math

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import QTimer, QTime, QDateTime

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
        self.controller = None
        self.position = 0.0
        self.actual_velocity = 0.0
        self.current_acceleration = 0.0
        self.previous_acceleration = 0.0
        self.cabin_temp = 25  # in Celsius

        # communicated values: Train Controller
        self.commanded_power = 0
        self.service_brakes = False
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

        # # For UI data and simulation state storage:
        # self.ui_data = {}
        # self.sim_state = {}
        
        # Set up timer for callback/update function
        self.prev_time = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

        # Minimal fix: Ensure a backend attribute exists.
        self.backend = self

    # This method uses self.ui_data to do physics.
    def update(self):
        # do physics, ur storing all the data anyways
        # commanded_speed = self.ui_data.get("commanded_speed", 0.0)
        # commanded_power = self.ui_data.get("commanded_power", 0.0)
        # speed_limit = self.ui_data.get("speed_limit", 0.0)
        # grade = self.ui_data.get("grade", 0.0)
        # mass_kg = self.ui_data.get("mass_kg", 0.0)
        # service_brakes = self.ui_data.get("service_brakes", False)
        # heat_signal = self.ui_data.get("heat_signal", False)
        # ac_signal = self.ui_data.get("ac_signal", False)
        # emergency_active = self.ui_data.get("emergency_brake", False)
        
        # if self.current_train:
        current_time = QDateTime.currentMSecsSinceEpoch()
        if self.prev_time is None:
            self.prev_time = current_time
            return
        dt = (current_time - self.prev_time) / 1000.0
        self.prev_time = current_time

        try:
            v_eff = self.actual_velocity if self.actual_velocity > 0.001 else 0.001
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
        elif self.service_brakes:
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

        old_velocity = self.actual_velocity
        new_velocity = old_velocity + (dt / 2.0) * (final_acceleration + self.previous_acceleration)
        if new_velocity < 0:
            new_velocity = 0

        self.previous_acceleration = final_acceleration
        self.actual_velocity = new_velocity
        self.current_acceleration = final_acceleration

        brake_off = (not self.driver_emergency_brake) and (not self.service_brakes)
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
        self.cabin_temp += dtemp
        display_temp = (self.cabin_temp * 1.8) + 32

        return {
            "acceleration": final_acceleration,
            "velocity": new_velocity,
            "cabin_temp": display_temp
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

            self.service_brakes = selected_data["service_brakes"]
            self.driver_emergency_brake = selected_data["emergency_active"]
            self.cabin_lights = selected_data["int_lights"]
            self.headlights = selected_data["ext_lights"]
            self.left_doors = selected_data["left_doors"]
            self.right_doors = selected_data["right_doors"]
            self.announcement = selected_data["announcements"]
            self.heating = selected_data["heat_signal"]
            self.air_conditioning = selected_data["ac_signal"]
            
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