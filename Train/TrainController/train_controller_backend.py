"""
Author: Aragya Goyal
Date: 03-20-2025
Description:

"""

class TrainController:
    def __init__(self, model):
        self.model = model
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
        self.manual_mode = False

        # Default for power calculation
        self.integral_error = 0.0
        self.Kp = 1.0
        self.Ki = 1.0

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
            if (self.commanded_wayside_speed > self.speed_limit):
                # Unsafe
                self.error = self.speed_limit - self.actual_speed
            else:
                # Safe
                self.error = self.commanded_wayside_speed - self.actual_speed
            
        self.integral_error += self.error * (0.001) # TODO: THIS SHOULD BE A DT CONSTANT THAT CHANGES THE RATE AT WHICH UPDATE FUNCTION ALSO RUNS
        self.commanded_power = (self.Kp * self.error) + (self.Ki * self.integral_error) # TODO: need something for integral wind up

        # Check for invalid power commands
        if (self.commanded_power < 0):
            self.commanded_power = 0.0
            self.service_brake = True
        elif (self.commanded_power > 120000):
            self.commanded_power = 120000.0
        else:
            self.service_brake = False

        if (self.emergency_brake):
            self.commanded_power = 0.0 # Kill engine if emergency brake is activated

        # Set the HVAC Signals
        self.activate_air_conditioning() if self.temperature_status > self.desired_temperature else self.deactivate_air_conditioning()
        self.activate_heating() if self.temperature_status < self.desired_temperature else self.deactivate_heating()

        # Check time for lights
        if (not self.manual_mode):
            print("FIX TIME THING IN BACKEND END UPDATE")
            hour = 0#self.simulated_time.hour()
            if (hour >= 19 and hour <= 24) or (hour >= 0 and hour < 7):
                self.activate_interior_lights()
                self.activate_headlights()
            else:
                self.deactivate_interior_lights()
                self.deactivate_headlights()