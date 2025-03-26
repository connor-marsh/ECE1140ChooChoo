# backend.py

import math

class TrainModel:
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

        # communicated values: Track Model
        self.wayside_speed = 0
        self.wayside_authority = 0
        self.beacon_data = ""

        # # For UI data and simulation state storage:
        # self.ui_data = {}
        # self.sim_state = {}

        # Minimal fix: Ensure a backend attribute exists.
        self.backend = self

    # This method uses self.ui_data to do physics.
    def update(self, dt):
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

        try:
            v_eff = self.actual_velocity if self.actual_velocity > 0.001 else 0.001
            dyn_force = self.commanded_power / v_eff
        except ZeroDivisionError:
            dyn_force = 1000.0

        theta = math.atan(self.grade / 100.0)
        grav_force = self.mass_kg * self.GRAVITY * math.sin(theta)
        net_force = dyn_force - grav_force
        a_base = net_force / self.mass_kg if self.mass_kg != 0 else 0.0

        if self.emergency_active:
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

        brake_off = (not self.emergency_active) and (not self.service_brakes)
        if brake_off and new_velocity < self.MIN_SPEED_NO_BRAKE:
            new_velocity = self.MIN_SPEED_NO_BRAKE

        # Temperature control logic
        degrees_per_second = 0.005
        if self.heat_signal and not self.ac_signal:
            dtemp = degrees_per_second * dt
        elif self.ac_signal and not self.heat_signal:
            dtemp = -degrees_per_second * dt
        elif self.ac_signal and self.heat_signal:
            dtemp = 0.0
        else:
            dtemp = 0.0005
        self.cabin_temp += dtemp
        display_temp = (self.cabin_temp * 1.8) + 32

        return {
            "acceleration": final_acceleration,
            "velocity": new_velocity,
            "cabin_temp": display_temp
        }
    
    def update_from_testbench(self, wayside_data, lights_doors_data, train_physical_data, emergency_active):
        # Have it so that whatever data is entered in testbench gets stored in the variables, which gets then gets called in the frontend
        self.commanded_power = wayside_data["commanded_power"]
        self.service_brakes = lights_doors_data["service_brakes"]
        self.driver_emergency_brake = emergency_active
        self.cabin_lights = lights_doors_data["int_lights"]
        self.headlights = lights_doors_data["ext_lights"]
        self.left_doors = lights_doors_data["left_doors"]
        self.right_doors = lights_doors_data["right_doors"]
        self.announcement = lights_doors_data["announcements"]
        self.wayside_speed = train_physical_data["commanded_speed"]
        self.wayside_authority = train_physical_data["authority"]
        self.beacon_data = train_physical_data["beacon_data"]

        # # Merge the data from the testbench into a single dictionary and store in ui_data.
        # merged = {}
        # merged.update(wayside_data)
        # merged.update(lights_data)
        # merged.update(physical_data)
        # merged['emergency_brake'] = emergency_active
        # self.ui_data = merged
