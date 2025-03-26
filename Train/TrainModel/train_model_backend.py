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

        # For UI data and simulation state storage:
        self.ui_data = {}
        self.sim_state = {}

        # Minimal fix: Ensure a backend attribute exists.
        self.backend = self

    # This method uses self.ui_data to do physics.
    def update(self, dt):
        # do physics, ur storing all the data anyways
        commanded_speed = self.ui_data.get("commanded_speed", 0.0)
        commanded_power = self.ui_data.get("commanded_power", 0.0)
        speed_limit = self.ui_data.get("speed_limit", 0.0)
        grade = self.ui_data.get("grade", 0.0)
        mass_kg = self.ui_data.get("mass_kg", 0.0)
        service_brakes = self.ui_data.get("service_brakes", False)
        heat_signal = self.ui_data.get("heat_signal", False)
        ac_signal = self.ui_data.get("ac_signal", False)
        emergency_active = self.ui_data.get("emergency_brake", False)

        try:
            v_eff = self.actual_velocity if self.actual_velocity > 0.001 else 0.001
            dyn_force = commanded_power / v_eff
        except ZeroDivisionError:
            dyn_force = 1000.0

        theta = math.atan(grade / 100.0)
        grav_force = mass_kg * self.GRAVITY * math.sin(theta)
        net_force = dyn_force - grav_force
        a_base = net_force / mass_kg if mass_kg != 0 else 0.0

        if emergency_active:
            target_a = self.EMERGENCY_DECEL - self.GRAVITY * math.sin(theta)
            self.current_acceleration = target_a
        elif service_brakes:
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

        a = self.current_acceleration
        if a > self.MAX_ACCEL:
            a = self.MAX_ACCEL
        elif a < -self.MAX_ACCEL:
            a = -self.MAX_ACCEL

        old_velocity = self.actual_velocity
        new_velocity = old_velocity + (dt / 2.0) * (a + self.previous_acceleration)
        if new_velocity < 0:
            new_velocity = 0

        self.previous_acceleration = a
        self.actual_velocity = new_velocity
        self.current_acceleration = a

        brake_off = (not emergency_active) and (not service_brakes)
        if brake_off and new_velocity < self.MIN_SPEED_NO_BRAKE:
            new_velocity = self.MIN_SPEED_NO_BRAKE

        # Temperature control logic
        degrees_per_second = 0.005
        if heat_signal and not ac_signal:
            dtemp = degrees_per_second * dt
        elif ac_signal and not heat_signal:
            dtemp = -degrees_per_second * dt
        elif ac_signal and heat_signal:
            dtemp = 0.0
        else:
            dtemp = 0.0005
        self.cabin_temp += dtemp
        display_temp = (self.cabin_temp * 1.8) + 32

        return {
            "acceleration": a,
            "velocity": new_velocity,
            "cabin_temp": display_temp
        }
    
    def update_from_testbench(self, wayside_data, lights_data, physical_data, emergency_active):
        # Merge the data from the testbench into a single dictionary and store in ui_data.
        merged = {}
        merged.update(wayside_data)
        merged.update(lights_data)
        merged.update(physical_data)
        merged['emergency_brake'] = emergency_active
        self.ui_data = merged
