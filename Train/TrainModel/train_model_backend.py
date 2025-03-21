# backend.py
import math

class TrainSimulator:
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
        self.position = 0.0
        self.actual_velocity = 0.01  # Starting velocity (~2.24 mph)
        self.current_acceleration = 0.0
        self.previous_acceleration = 0.0
        self.cabin_temp = 25  # Cabin temperature in Celsius

    def update(self, dt, wayside_data, lights_doors_data, train_data, emergency_active):
        # Extract commanded and physical parameters
        commanded_speed = wayside_data["commanded_speed"]
        commanded_power_watts = wayside_data["commanded_power"]
        speed_limit = wayside_data["speed_limit"]

        mass_kg  = train_data["mass_kg"]
        grade    = train_data["grade"]

        try:
            v_eff = self.actual_velocity if self.actual_velocity > 0.1 else 0.1
            dyn_force = commanded_power_watts / v_eff
        except ZeroDivisionError:
            dyn_force = 1000.0

        theta = math.atan(grade / 100.0)  # Grade percent to radians
        grav_force = mass_kg * self.GRAVITY * math.sin(theta)
        net_force = dyn_force - grav_force
        a_base = net_force / mass_kg

        if emergency_active:
            target_a = self.EMERGENCY_DECEL - self.GRAVITY * math.sin(theta)
            self.current_acceleration = target_a
        elif lights_doors_data["service_brakes"]:
            target_a = self.SERVICE_DECEL - self.GRAVITY * math.sin(theta)
            ramp_rate = 1.0  # m/s³
            accel_diff = target_a - self.current_acceleration
            max_delta = ramp_rate * dt
            if abs(accel_diff) < max_delta:
                self.current_acceleration = target_a
            else:
                self.current_acceleration += math.copysign(max_delta, accel_diff)
        else:
            target_a = a_base
            ramp_rate = 1.0  # m/s³
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

        # threshold = 0.0001
        # if commanded_speed < threshold and commanded_power_watts < threshold:
        #     a = 0
        #     new_velocity = 0

        # Update previous acceleration for the next cycle.
        self.previous_acceleration = a

        # Update simulation state.
        self.actual_velocity = new_velocity
        self.current_acceleration = a

        # Ensure minimum velocity when brakes are off.
        brake_off = (not emergency_active) and (not lights_doors_data["service_brakes"])
        if brake_off and new_velocity < self.MIN_SPEED_NO_BRAKE:
            new_velocity = self.MIN_SPEED_NO_BRAKE

        # TEMPERATURE SETUP:
        # Define the environmental (ambient) temperature of the train car (in Celsius)
        T_env = 25.0

        # Get desired target temperature from the controller (in Celsius)
        # T_target = self.controller.desired_temperature
        T_target = 18.0 # Hardcoded target temperature

        # Calculate the error between the target and the current cabin temperature.
        error_temp = T_target - self.cabin_temp
        threshold = 1.0  # in Celsius; defines when to switch from active HVAC to ambient drift

        if abs(error_temp) > threshold:
            # Active HVAC: drive the temperature rapidly toward the target.
            k_active = 0.005  # gain for active adjustment (tune as needed)
            dtemp = k_active * error_temp * dt
        else:
            # When near the target, HVAC influence reduces and the temperature drifts slowly toward T_env.
            k_env = 0.01  # gain for natural drift (much smaller than active gain)
            dtemp = k_env * (T_env - self.cabin_temp) * dt

        self.cabin_temp += dtemp
        display_temp = (self.cabin_temp * 1.8) + 32  # Convert Celsius to Fahrenheit


        return {
            "acceleration": a,
            "velocity": new_velocity,
            "cabin_temp": display_temp
        }
